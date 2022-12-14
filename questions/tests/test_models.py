from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from questions.models import Comment, Question
from .utils import create_question

# Create your tests here.


class QuestionModelTest(TestCase):
    def test_questions_question_text_string_representation(self):
        needed_title = "Question one"
        author = User.objects.create_user(
            username="username", password="password")
        question = Question(question_text="Question one",
                            author=author)
        question.full_clean()
        question.save()

        self.assertEqual(str(question), needed_title)

    def test_question_absolute_url(self):
        question = create_question()
        self.client.get(
            reverse("questions:detail", kwargs={"pk": 1}))

        self.assertEqual(question.get_absolute_url(), "/question/1/detail/")


class CommentModelTest(TestCase):
    def test_comment_comment_text_string_representation(self):
        needed_title = "Comment 1"
        author = User.objects.create_user(
            username="username", password="password")
        comment = Comment(
            question=Question.objects.create(author=author),
            author=author,
            comment_text="Comment 1")
        comment.full_clean()
        comment.save()

        self.assertEqual(str(comment), needed_title)
