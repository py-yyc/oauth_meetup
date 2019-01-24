# Adding third-party sign-on to a Django site

 1. Run `docker-compose up --build`
 2. Go to the [Meetup Register OAuth Consumer page][oauth_create],
    enter anything for the consumer name, and
    `http://localhost:8000/oauth/login` for the ‘Redirect URI.’
 3. Add `MEETUP_CLIENT_ID` and `MEETUP_CLIENT_SECRET` to
   `.django_secrets.json`
 4. Visit http://localhost:8000/polls/

[create]: https://secure.meetup.com/meetup_api/oauth_consumers/create
