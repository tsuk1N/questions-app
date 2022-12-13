from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from . models import Comment, Question
from questions.views import (
    QuestionCreateView,
    QuestionDetailView,
    QuestionUpdateView
)

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
        view.get_success_url = url2
        url1 = reverse("questions:author-questions")
        response = self.client.post(
            view.get_success_url,
            data={"question_text": "what's is what is ?"})

        self.assertRedirects(response, url1)
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
