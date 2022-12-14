from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from parameterized import parameterized

from authors.forms import AuthorRegisterForm
from ..views import AuthorRegisterView

# Create your tests here.


class AuthorLoginViewTests(TestCase):
    def test_author_login_is_using_correct_template(self):
        response = self.client.get(
            reverse("authors:login"))
        self.assertTemplateUsed(response, "authors/author_login.html")

    def test_author_login_200_status(self):
        response = self.client.get(
            reverse("authors:login"))
        self.assertEqual(response.status_code, 200)

    def test_author_message_invalid_credentials(self):
        url = reverse("authors:login-create")
        response = self.client.post(url, data={
            "username": "username",
            "password": "password"
        })
        msgs = list(get_messages(response.wsgi_request))

        self.assertEqual(str(msgs[0]), "Invalid credentials")
        self.assertEqual(len(msgs), 1)

    def test_author_message_invalid_username_or_password(self):
        url = reverse("authors:login-create")
        response = self.client.post(url, data={
            "username": "",
            "password": ""
        })
        msgs = list(get_messages(response.wsgi_request))

        self.assertEqual(str(msgs[0]), "Invalid username or password")
        self.assertEqual(len(msgs), 1)

    def test_author_login(self):
        User.objects.create_user(username="username", password="passwords")
        url = reverse("authors:login-create")
        response = self.client.post(url, data={
            "username": "username",
            "password": "passwords",
        }, follow=True)

        self.assertIn("Welcome, username", response.content.decode("utf-8"))

    def test_author_login_404_if_get_request(self):
        url = reverse("authors:login-create")
        response = self.client.get(url)

        self.assertIn("Not Found", response.content.decode("utf-8"))
