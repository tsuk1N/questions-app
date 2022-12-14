from django.test import TestCase
from django.urls import reverse

from .utils import create_question

# Create your tests here.


class QuestionDeleteViewTests(TestCase):
    def setUp(self):
        self.q = create_question()
        return super().setUp()

    def test_question_delete_is_using_correct_template(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:delete", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "questions/question_delete.html")

    def test_question_delete_200_status(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:delete", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_question_is_successfully_deleted(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:delete", kwargs={"pk": 1})
        response = self.client.post(url, follow=True)

        self.assertNotContains(response, "Question number 1")
        self.assertNotIn("Question number 1", response.content.decode("utf-8"))

    def test_question_is_successfully_deleted_message(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:delete", kwargs={"pk": 1})
        response = self.client.post(url, follow=True)

        self.assertContains(
            response, "Your question was successfully deleted!")
        self.assertIn("Your question was successfully deleted!",
                      response.content.decode("utf-8"))

    def test_question_delete_view_returns_404_if_no_question_is_found(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:delete", kwargs={"pk": 1000})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_question_delete_is_showing_correct_question(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:delete", kwargs={"pk": 1}))
        self.assertEqual(
            response.context["question"].question_text, "Question number 1")
