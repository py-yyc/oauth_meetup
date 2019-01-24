import json

import requests
import responses
from django.http import HttpResponseRedirect, QueryDict
from django.test import TestCase, Client


class FakeOauthServer:
    def setup(self):
        responses.add_callback(responses.POST, "https://secure.meetup.com/oauth2/access",
                      callback=self.access)
        responses.add_callback(responses.GET, "https://api.meetup.com/2/member/self",
                      callback=self.member_self)

    def get_code(self):
        return "123abc"

    def _access_token(self):
        return "3209j09wajf"

    def access(self, request):
        body = QueryDict(request.body)
        # Currently the real client_secret is also used in the unit tests
        if body['code'] != self.get_code():
            return (401, {}, "Unauthorized")

        return (200, {}, json.dumps({
            "access_token": self._access_token(),
        }))

    def authorize_url(self):
        return self._url('/authorize')

    def member_self(self, request):
        if request.headers['Authorization'] != f"Bearer {self._access_token()}":
            return (401, {}, "Unauthorized")

        return (200, {}, json.dumps({
            "name": "user_foo bar",
            "id": 14390
        }))

class TestOauth(TestCase):
    @responses.activate
    def test_response_basics(self):
        """
        Testing out our HTTP-response mocking

        https://cra.mr/2014/05/20/mocking-requests-with-responses
        """
        responses.add(responses.GET, "https://example.org/hello",
                      body="Hello there pyyyc")
        response = requests.get("https://example.org/hello")
        self.assertIn("there pyyyc", response.text)

    def test_redirects_if_not_logged_in(self):
        s = FakeOauthServer()

        c = Client()
        response = c.get('/oauth/login')

        self.assertEquals(response.status_code, HttpResponseRedirect.status_code)
        self.assertTrue(response['Location'].startswith('https://secure.meetup.com/oauth2/authorize?'))

    @responses.activate
    def test_oauth_login(self):
        s = FakeOauthServer()
        s.setup()

        c = Client()
        response = c.get('/oauth/login?code=123abc', follow=True)

        self.assertContains(response, "user_foo bar")

        return c

    def test_oauth_login_stored_in_session(self):
        c = self.test_oauth_login()

        # Should be logged in now for other urls in the same session
        response = c.get("/polls/")
        self.assertContains(response, "user_foo bar")
        self.assertContains(response, "Log out")

