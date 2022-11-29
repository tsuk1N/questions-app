from django.contrib import admin

from . models import Question, Comment
# Register your models here.


@admin.action(description="Mark questions as published")
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Mark questions as not published")
def make_not_published(modeladmin, request, queryset):
    queryset.update(is_published=False)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class QuestionInline(admin.ModelAdmin):
    inlines = [CommentInline, ]
    list_display = ("question_text", "author", "pub_date", "is_published")
    search_fields = ["question_text"]
    list_filter = ["pub_date", "is_published", ]
    actions = [make_published, make_not_published]
    list_per_page = 20


admin.site.register(Question, QuestionInline)
