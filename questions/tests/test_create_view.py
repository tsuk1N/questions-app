from django.test import TestCase
from django.urls import reverse

from .utils import create_question

from questions.views import (
    QuestionCreateView,
)

# Create your tests here.


class QuestionCreateViewTests(TestCase):
    def setUp(self):
        self.q = create_question()
        return super().setUp()

    def test_question_create_is_using_correct_template(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:create"))
        self.assertTemplateUsed(response, "questions/question_create.html")

    def test_question_create_200_status(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:create"))
        self.assertEqual(response.status_code, 200)

    def test_question_create_must_have_more_than_15_characters(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:create")
        response = self.client.post(
            url, data={"question_text": "question1234567"})
        self.assertIn("Your question must have more than 15 characters.",
                      response.content.decode("utf-8"))
        self.assertContains(response,
                            "Your question must have more than 15 characters.")

    def test_question_create_form_valid_and_success_url(self):
        self.client.login(username="username", password="password")
        view = QuestionCreateView()
        url2 = reverse("questions:create")
        response = self.client.post(
            url2,
            data={"question_text": "what's is what is ?"})

        self.assertRedirects(response, view.get_success_url())
        self.assertEqual(response.status_code, 302)

    def test_question_create_form_invalid(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:create")
        response = self.client.post(url, data={"question_text": " "})

        self.assertIn("This field is required.",
                      response.content.decode("utf-8"))
        self.assertContains(response, "This field is required.")

    def test_question_create_is_posted(self):
        self.client.login(username="username", password="password")
        url1 = reverse("questions:create")
        url2 = reverse("questions:author-questions")
        response = self.client.post(
            url1, data={"question_text": "questiontext1234"}, follow=True)

        self.assertRedirects(response, url2)
        self.assertIn("questiontext1234", response.content.decode("utf-8"))
        self.assertContains(response, "questiontext1234")

    def test_question_create_template_shows_login_message(self):
        response = self.client.get(reverse("questions:create"))
        self.assertIn('You need to login first to make your question.',
                      response.content.decode("utf-8"))
        self.assertContains(
            response, 'You need to login first to make your question.')
