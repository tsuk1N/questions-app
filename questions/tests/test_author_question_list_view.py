from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from questions.models import Question
from . utils import create_question


# Create your tests here.


class AuthorQuestionListViewTests(TestCase):
    def test_author_question_list_is_using_correct_template(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:author-questions"))
        self.assertTemplateUsed(
            response, "questions/author_question_list.html")

    def test_author_question_list_200_status(self):
        self.client.login(username="username", password="password")
        response = self.client.get(
            reverse("questions:author-questions"))
        self.assertEqual(response.status_code, 200)

    def test_author_question_list_has_no_questions(self):
        User.objects.create_user(username="username", password="password")
        self.client.login(username="username", password="password")
        response = self.client.get(reverse("questions:author-questions"))
        self.assertIn(
            "No questions to show", response.content.decode("utf-8"))
        self.assertQuerysetEqual(response.context["question_list"], [])

    def test_author_question_list_has_a_question(self):
        question = create_question()
        self.client.login(username="username", password="password")
        response = self.client.get(reverse("questions:author-questions"))
        self.assertQuerysetEqual(response.context["question_list"], [question])

    def test_author_question_list_has_more_than_1_question(self):
        author = User.objects.create_user(
            username="username1", password="password")
        self.client.login(username="username1", password="password")
        q1 = Question.objects.create(
            question_text="Question number 1", author=author)
        q2 = Question.objects.create(
            question_text="Question number 2", author=author)

        response = self.client.get(reverse("questions:author-questions"))
        self.assertIn(str(q1), response.content.decode("utf-8"))
        self.assertIn(str(q2), response.content.decode("utf-8"))

    def test_author_question_list_template_shows_login_message(self):
        response = self.client.get(reverse("questions:author-questions"))
        self.assertIn('You need to login first to see your questions.',
                      response.content.decode("utf-8"))
        self.assertContains(
            response, 'You need to login first to see your questions.')

    def test_author_question_list_template_shows_message_if_no_questions(self):
        User.objects.create_user(username="username", password="password")
        self.client.login(username="username", password="password")
        response = self.client.get(reverse("questions:author-questions"))
        self.assertContains(response, "No questions to show")
        self.assertIn("No questions to show", response.content.decode("utf-8"))

    def test_author_question_list_dont_show_published_questions(self):
        create_question(is_published=True)
        self.client.login(username="username", password="password")
        response = self.client.get(reverse("questions:author-questions"))

        self.assertIn("No questions to show", response.content.decode("utf-8"))
        self.assertContains(response, "No questions to show")
