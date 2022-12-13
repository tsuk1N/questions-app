from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class AuthorLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
        error_messages={
            "required": "Input your username",
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        error_messages={
            "required": "Input your password",
        },
        strip=False,
    )


class AuthorRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    username = forms.CharField(
        required=True,
        error_messages={
            "required": "Username is required",
            "min_length": "Username must have 5 or more characters.",
            "max_length": "Username must have 30 or less characters.",
        },
        widget=forms.TextInput(attrs={"placeholder": "Write your username"}),
        label="Username *",
        help_text="Username must have between 5 and 30 characters."
        " No special characters allowed, except: @/./+/-/_",
        min_length=5, max_length=30,
    )

    first_name = forms.CharField(
        required=False,
        label="First Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Write your first name"}))

    last_name = forms.CharField(
        required=False,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"placeholder": "Write your last name"}))

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Input a valid e-mail"}),
        label="E-Mail *"
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Input your password"}),
        error_messages={
            "required": "Password is required"
        },
        label="Password *",
        help_text="Your password must have more than 8 characters.",
        strip=False,
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repeat your password"}),
        error_messages={
            "required": "Need to repeat your password"
        },
        label="Repeat your password *",
        strip=False,
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError("E-mail is already in use.", code="invalid")

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        exists = User.objects.filter(username=username).exists()

        if exists:
            raise ValidationError(
                "Username is already in use.", code="invalid")

        return username

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2 or len(password) < 8 and len(password) > 30:
            password_confirmation_error = ValidationError(
                "Passwords must be equal.",
                code="invalid")

            raise ValidationError({
                "password": password_confirmation_error,
                "password2": [password_confirmation_error, ]
            })

        elif len(password) <= 8 or len(password) > 30:
            password_confirmation_error = ValidationError(
                "Passwords must have more than 8 and less than 30 characters.",
                code="invalid")

            raise ValidationError({
                "password": password_confirmation_error,
                "password2": [password_confirmation_error, ]
            })
