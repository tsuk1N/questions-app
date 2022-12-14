from django.contrib.auth.models import User

from questions.models import Comment, Question

# Create your tests here.


def create_question(question_text="Question number 1", is_published=False,
                    username="username"):
    author = User.objects.create_user(
        username=username, password="password")
    question = Question.objects.create(
        author=author, question_text=question_text, is_published=is_published)

    return question


def create_comment(comment_text="commenttext"):
    author = User.objects.create_user(
        username="username1", password="password1")
    question = Question.objects.create(author=author, question_text="Question")
    comment = Comment.objects.create(question=question,
                                     author=author,
                                     comment_text=comment_text)

    return comment
