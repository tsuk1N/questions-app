from django import forms
from django.core.exceptions import ValidationError

from . models import Comment, Question


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment_text", ]
        widgets = {
            "comment_text": forms.Textarea(attrs={
                "placeholder": "Write your answer here..."
            })
        }

    def clean_comment_text(self):
        ct = self.cleaned_data["comment_text"]

        if len(ct) <= 3:
            raise ValidationError(
                "Your comment must have more than 3 characters.",
                code="invalid")

        return ct


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text", ]
        widgets = {
            "question_text": forms.Textarea(attrs={
                "placeholder": "Write your question here..."
            })
        }

    def clean_question_text(self):
        qt = self.cleaned_data["question_text"]

        if len(qt) <= 15:
            raise ValidationError(
                "Your question must have more than 15 characters.", code="invalid")

        return qt
