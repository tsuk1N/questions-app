from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Question(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question_text = models.CharField(max_length=150)
    pub_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("questions:detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(
        Question, null=True, on_delete=models.SET_NULL, related_name="comment")
    comment_text = models.TextField("", max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.comment_text[:20]
