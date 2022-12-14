from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from questions.models import Question
from .utils import create_question


# Create your tests here.


class QuestionsIndexViewTest(TestCase):
    def test_index_is_using_correct_template(self):
        response = self.client.get(reverse("questions:list"))
        self.assertTemplateUsed(response, "questions/question_list.html")

    def test_index_200_status(self):
        response = self.client.get(reverse("questions:list"))
        self.assertEqual(response.status_code, 200)

    def test_index_has_no_questions(self):
        response = self.client.get(reverse("questions:list"))
        self.assertContains(
            response, "No questions to show")
        self.assertQuerysetEqual(response.context["question_list"], [])

    def test_index_has_a_question(self):
        question = create_question(is_published=True)
        self.client.login(username="username", password="password")
        response = self.client.get(reverse("questions:list"))
        self.assertQuerysetEqual(response.context["question_list"], [question])

    def test_index_has_more_than_1_question(self):
        author = User.objects.create_user(
            username="username1", password="password")
        q1 = Question.objects.create(
            question_text="Question number 1", author=author,
            is_published=True)
        q2 = Question.objects.create(
            question_text="Question number 2", author=author,
            is_published=True)

        response = self.client.get(reverse("questions:list"))
        self.assertIn(str(q1), response.content.decode("utf-8"))
        self.assertIn(str(q2), response.content.decode("utf-8"))

    def test_index_template_shows_no_question_to_show_if_no_questions(self):
        response = self.client.get(reverse("questions:list"))
        self.assertContains(response, "No questions to show")
        self.assertIn("No questions to show", response.content.decode("utf-8"))

    def test_index_template_dont_show_questions_not_published(self):
        create_question()
        response = self.client.get(reverse("questions:list"))

        self.assertIn("No questions to show", response.content.decode("utf-8"))
        self.assertContains(response, "No questions to show")
