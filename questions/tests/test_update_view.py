from django.test import TestCase
from django.urls import reverse

from .utils import create_question

from questions.views import (
    QuestionUpdateView,
)

# Create your tests here.


class QuestionUpdateViewTests(TestCase):
    def setUp(self):
        self.q = create_question()
        return super().setUp()

    def test_question_update_is_using_correct_template(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:update", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "questions/question_update.html")

    def test_question_update_200_status(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:update", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_question_update_must_have_more_than_15_characters(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:update", kwargs={"pk": 1})
        response = self.client.post(
            url, data={"question_text": "question1234567"})
        self.assertIn("Your question must have more than 15 characters.",
                      response.content.decode("utf-8"))
        self.assertContains(response,
                            "Your question must have more than 15 characters.")

    def test_question_update_form_valid_and_success_url(self):
        self.client.login(username="username", password="password")
        view = QuestionUpdateView()
        url2 = reverse("questions:update", kwargs={"pk": 1})
        view.get_success_url = url2
        url1 = reverse("questions:detail", kwargs={"pk": 1})
        response = self.client.post(
            view.get_success_url,
            data={"question_text": "what's is what is ?"})

        self.assertRedirects(response, url1)
        self.assertEqual(response.status_code, 302)

    def test_question_update_form_invalid(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:update", kwargs={"pk": 1})
        response = self.client.post(url, data={"question_text": " "})

        self.assertIn("This field is required.",
                      response.content.decode("utf-8"))
        self.assertContains(response, "This field is required.")

    def test_question_is_updated_and_posted(self):
        create_question(is_published=True, username="username1")
        self.client.login(username="username", password="password")
        url1 = reverse("questions:update", kwargs={"pk": 2})
        url2 = reverse("questions:detail", kwargs={"pk": 2})
        response = self.client.post(
            url1, data={"question_text": "questiontext1234"}, follow=True)

        self.assertRedirects(response, url2)
        self.assertIn("questiontext1234", response.content.decode("utf-8"))
        self.assertContains(response, "questiontext1234")

    def test_question_update_view_returns_404_if_no_question_is_found(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:update", kwargs={"pk": 1000})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
