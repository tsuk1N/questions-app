from django.test import TestCase
from django.urls import reverse

from .utils import create_question


class PaginationTest(TestCase):
    def setUp(self):
        for i in range(15):
            create_question(
                question_text=f"Question number {i}",
                username=f"username {i}",
                is_published=True
            )
        return super().setUp()

    def test_pagination_has_ten_questions_on_the_first_page(self):
        response = self.client.get(reverse("questions:list"))
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["question_list"]), 10)

    def test_pagination_show_last_5_questions_on_page_2(self):
        response = self.client.get(reverse("questions:list")+"?page=2")
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["question_list"]), 5)
