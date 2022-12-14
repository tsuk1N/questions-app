from django.test import TestCase
from django.urls import reverse

from .utils import create_question

from questions.views import (
    QuestionDetailView,
)

# Create your tests here.


class QuestionDetailViewTests(TestCase):
    def setUp(self):
        create_question(is_published=True)
        return super().setUp()

    def test_question_detail_is_using_correct_template(self):
        response = self.client.get(
            reverse("questions:detail", kwargs={"pk": 1}))
        self.assertTemplateUsed(response, "questions/question_detail.html")

    def test_question_detail_200_status(self):
        response = self.client.get(
            reverse("questions:detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)

    def test_question_detail_is_showing_correct_question(self):
        response = self.client.get(
            reverse("questions:detail", kwargs={"pk": 1}))
        self.assertEqual(
            response.context["question"].question_text, "Question number 1")

    def test_question_detail_view_returns_404_if_no_question_is_found(self):
        url = reverse("questions:detail", kwargs={"pk": 1000})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_question_detail_template_shows_login_message_to_comment(self):
        response = self.client.get(
            reverse("questions:detail", kwargs={"pk": 1}))
        self.assertIn('You must login to write an answer.',
                      response.content.decode("utf-8"))
        self.assertContains(
            response, 'You must login to write an answer.')

    def test_question_detail_comment_form_valid_and_success_url(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:detail", kwargs={"pk": 1})
        view = QuestionDetailView()
        view.get_success_url = url
        response = self.client.post(view.get_success_url, data={
            "comment_text": "commenttext",
        })

        self.assertRedirects(response, url)
        self.assertEqual(response.status_code, 302)

    def test_question_detail_comment_form_invalid(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:detail", kwargs={"pk": 1})
        response = self.client.post(url, data={
            "comment_text": " ",
        })

        self.assertIn("This field is required.",
                      response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)

    def test_question_detail_comment_is_posted(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:detail", kwargs={"pk": 1})
        response = self.client.post(url,
                                    data={"comment_text": "commenttext"},
                                    follow=True)

        self.assertIn("commenttext", response.content.decode("utf-8"))
        self.assertContains(response, "commenttext")

    def test_question_detail_comment_must_have_more_than_3_characters(self):
        self.client.login(username="username", password="password")
        url = reverse("questions:detail", kwargs={"pk": 1})
        response = self.client.post(url, data={"comment_text": "yes"})

        self.assertIn("Your comment must have more than 3 characters.",
                      response.content.decode("utf-8"))
        self.assertContains(
            response, "Your comment must have more than 3 characters.")

    def test_question_detail_comment_message_if_no_comments(self):
        url = reverse("questions:detail", kwargs={"pk": 1})
        response = self.client.get(url)

        self.assertIn("Be the first one to write an answer!",
                      response.content.decode("utf-8"))
        self.assertContains(response, "Be the first one to write an answer!")

    def test_question_detail_question_not_found_message_if_not_published(self):
        create_question(is_published=False, username="username1")

        response = self.client.get(
            reverse("questions:detail", kwargs={"pk": 2}))

        self.assertContains(response, "Question not found")
        self.assertIn("Question not found", response.content.decode("utf-8"))
