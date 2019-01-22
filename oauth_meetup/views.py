import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def oauth(request):
    redirect_uri = request.build_absolute_uri(reverse('meetup_oauth:login'))

    if 'code' not in request.GET:
        qd = QueryDict(mutable=True)
        qd['client_id'] = settings.MEETUP_CLIENT_ID
        qd['response_type'] = 'code'
        qd['redirect_uri'] = redirect_uri
        return redirect(f"https://secure.meetup.com/oauth2/authorize?{qd.urlencode()}")

    access_response = requests.post("https://secure.meetup.com/oauth2/access", {
        "client_id": settings.MEETUP_CLIENT_ID,
        "client_secret": settings.MEETUP_CLIENT_SECRET,
        "grant_type": "authorization_code",
        # This is a copy of what was sent earlier, not where to go after this.
        "redirect_uri": redirect_uri,
        "code": request.GET['code'],
    })

    # TODO: save access response in DB for future calls, refreshing token, ...
    access_token = access_response.json()['access_token']

    lookup_self_response = requests.get('https://api.meetup.com/2/member/self', headers={
        "Authorization": f"Bearer {access_token}",
    })
    user_info = lookup_self_response.json()
    print(user_info)

    # TODO: save user data in new DB model
    try:
        user = User.objects.get(username=f"{user_info['id']}@meetup.com")
    except User.DoesNotExist:
        user = User(username=f"{user_info['id']}@meetup.com",
                    first_name=user_info['name'])
        user.save()
    login(request, user)
    return HttpResponseRedirect('/polls/')


def logout(request):
    return LogoutView.as_view()(request)
