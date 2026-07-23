from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Item, Loan


class InventoryViewsTests(TestCase):
    def setUp(self):
        self.item = Item.objects.create(
            name="テスト用ノートPC",
            category="IT機器",
            total_quantity=2,
            location="職員室",
        )

    def test_dashboard_displays_item_and_available_quantity(self):
        Loan.objects.create(
            item=self.item,
            borrower_name="山田 太郎",
            due_date=timezone.localdate() + timedelta(days=7),
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "テスト用ノートPC")
        self.assertContains(response, "<b>1</b> / 2", html=True)

    def test_returning_a_loan_records_return_time(self):
        loan = Loan.objects.create(
            item=self.item,
            borrower_name="山田 太郎",
            due_date=timezone.localdate() + timedelta(days=7),
        )

        response = self.client.post(reverse("return_loan", args=[loan.pk]))

        self.assertRedirects(response, reverse("loan_list"))
        loan.refresh_from_db()
        self.assertIsNotNone(loan.returned_at)
