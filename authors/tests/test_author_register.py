from django.test import TestCase
from django.urls import reverse

from authors.views import AuthorRegisterView
from authors.forms import AuthorRegisterForm

from parameterized import parameterized


class AuthorRegisterViewTests(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            "username": "username",
            "first_name": "user",
            "last_name": "name",
            "email": "email@email.com",
            "password": "passwords",
            "password2": "passwords"
        }

        return super().setUp(*args, **kwargs)

    def test_author_register_is_using_correct_template(self):
        response = self.client.get(
            reverse("authors:register"))
        self.assertTemplateUsed(response, "authors/author_register.html")

    def test_author_register_200_status(self):
        response = self.client.get(
            reverse("authors:register"))
        self.assertEqual(response.status_code, 200)

    def test_author_registration_form_is_valid_and_success_url(self):
        view = AuthorRegisterView()
        url = reverse("authors:register")
        url2 = view.get_success_url()
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn("Your user was successfully created. "
                      "You can log in now!",
                      response.content.decode("utf-8"))
        self.assertRedirects(response, url2)

    @parameterized.expand([
        ("username", "Username must have between 5 and 30 characters. "
         "No special characters allowed, except: @/./+/-/_"),
        ("password", "Your password must have more than 8 characters."),
    ])
    def test_fields_help_text(self, field, needed):
        form = AuthorRegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    def test_username_min_length_should_be_5(self):
        self.form_data["username"] = "user"
        url = reverse("authors:register")
        msg = "Username must have 5 or more characters."
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))

    def test_username_max_length_should_be_30(self):
        self.form_data["username"] = "u" * 31
        url = reverse("authors:register")
        msg = "Username must have 30 or less characters."
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("username"))

    def test_password_must_have_more_than_8_characters(self):
        self.form_data["password"] = "password"
        self.form_data["password2"] = "password"
        url = reverse("authors:register")
        msg = "Passwords must have more than 8 and less than 30 characters."
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("password"))

    def test_password_must_have_less_than_30_characters(self):
        self.form_data["password"] = "password" * 4
        self.form_data["password2"] = "password" * 4
        url = reverse("authors:register")
        msg = "Passwords must have more than 8 and less than 30 characters."
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("password"))

    def test_passwords_must_be_equal(self):
        self.form_data["password"] = "passwordw"
        self.form_data["password2"] = "passwords"
        url = reverse("authors:register")
        msg = "Passwords must be equal."
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("password"))

    def test_email_must_be_unique(self):
        url = reverse("authors:register")
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "E-mail is already in use."

        self.assertIn(msg, response.content.decode("utf-8"))
        self.assertIn(msg, response.context["form"].errors.get("email"))

    def test_author_created_can_login(self):
        self.client.post(
            reverse("authors:register"), data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username="username", password="passwords")

        self.assertTrue(is_authenticated)
