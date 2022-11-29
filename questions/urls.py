from django.urls import path

from . views import QuestionCreateView, QuestionDeleteView, QuestionDetailView, QuestionListView, QuestionUpdateView

app_name = "questions"

urlpatterns = [
    path("question/<int:pk>/detail/", QuestionDetailView.as_view(),
         name="detail"),
    path("question/<int:pk>/update/", QuestionUpdateView.as_view(),
         name="update"),
    path("question/<int:pk>/delete/", QuestionDeleteView.as_view(),
         name="delete"),
    path("question/create/", QuestionCreateView.as_view(), name="create"),
    path("", QuestionListView.as_view(), name="list"),
]
