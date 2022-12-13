from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView,
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .models import Question
from . forms import CommentForm, QuestionForm

# Create your views here.


class QuestionListView(ListView):
    model = Question
    context_object_name = "question_list"
    template_name = "questions/question_list.html"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Question.objects.filter(is_published=True)
        return qs


class QuestionDetailView(DetailView, FormMixin):
    model = Question
    context_object_name = "question"
    template_name = "questions/question_detail.html"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_comment = form.save(commit=False)
        form.instance.question = self.object
        form.instance.author = self.request.user
        new_comment.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questions:detail", kwargs={"pk": self.object.pk})


class QuestionCreateView(CreateView):
    model = Question
    template_name = "questions/question_create.html"
    context_object_name = "comment"
    form_class = QuestionForm

    def form_valid(self, form):
        new_question = form.save(commit=False)
        form.instance.author = self.request.user
        new_question.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questions:author-questions")


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = "questions/question_update.html"
    context_object_name = "question"
    form_class = QuestionForm

    def form_valid(self, form):
        new_question = form.save(commit=False)
        form.instance.author = self.request.user
        new_question.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questions:detail", kwargs={"pk": self.object.pk})


class QuestionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Question
    template_name = "questions/question_delete.html"
    context_object_name = "question"
    success_message = "Your question was successfully deleted!"

    def get_success_url(self):
        return reverse_lazy("questions:list")


class AuthorQuestionListView(ListView):
    model = Question
    context_object_name = "question_list"
    template_name = "questions/author_question_list.html"
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Question.objects.filter(
            author=self.request.user.id, is_published=False)
        return qs
