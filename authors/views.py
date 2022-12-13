from . forms import AuthorLoginForm, AuthorRegisterForm
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# Create your views here.

def login_view(request):
    form = AuthorLoginForm()

    return render(request, "authors/author_login.html", {
        "form": form,
        "form_action": reverse("authors:login-create")
    })


def login_create(request):
    if not request.method == "POST":
        raise Http404()

    form = AuthorLoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get("username", ""),
            password=form.cleaned_data.get("password", ""),
        )
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect(reverse("questions:list"))
        else:
            messages.error(request, "Invalid credentials")
    else:
        messages.error(request, "Invalid username or password")
    return redirect(reverse("authors:login"))


class AuthorRegisterView(SuccessMessageMixin, CreateView):
    template_name = "authors/author_register.html"
    form_class = AuthorRegisterForm
    success_message = "Your user was successfully created. You can log in now!"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questions:list")

# TODO separar os testes em arquivos diferentes e criar pasta tests para questions e authors
