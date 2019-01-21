from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Poll, Choice

class BasicPollsTests(TestCase):
    def setup_poll1(self):
        poll = Poll(question='Which is better?', pub_date=timezone.now())
        poll.save()

        email_choice = Choice(question=poll, choice_text='Email sign-up')
        email_choice.save()

        external_choice = Choice(question=poll, choice_text='External sign-in')
        external_choice.save()

        return (poll, email_choice, external_choice)

    def test_empty_polls_index(self):
        c = Client()
        response = c.get('/polls/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

    def test_index_shows_a_poll(self):
        q, c1, c2 = self.setup_poll1()

        c = Client()
        response = c.get('/polls/')

        self.assertEquals(response.status_code, 200)
        self.assertContains(response, q.question)

    def test_view_poll_detail(self):
        q, c1, c2 = self.setup_poll1()

        c = Client()
        response = c.get(reverse('polls:detail', args=[q.id]))

        self.assertContains(response, c1.choice_text)
        self.assertContains(response, c2.choice_text)

    def test_can_vote(self):
        q, c1, c2 = self.setup_poll1()

        c = Client()
        response = c.post(reverse('polls:vote', args=[q.id]), {
            "choice": c1.id
        })

        self.assertRedirects(response, reverse('polls:results', args=[q.id]))

        c1.refresh_from_db()
        self.assertEquals(1, c1.votes)
