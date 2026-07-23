from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField("備品名", max_length=100)
    category = models.CharField("カテゴリ", max_length=50)
    total_quantity = models.PositiveIntegerField("所持数", default=1)
    location = models.CharField("保管場所", max_length=100, blank=True)
    notes = models.TextField("備考", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name

    @property
    def loaned_quantity(self):
        return self.loans.filter(returned_at__isnull=True).count()

    @property
    def available_quantity(self):
        return self.total_quantity - self.loaned_quantity


class Loan(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="loans", verbose_name="備品")
    borrower_name = models.CharField("借りた人", max_length=100)
    due_date = models.DateField("返却予定日")
    loaned_at = models.DateTimeField("貸出日時", default=timezone.now)
    returned_at = models.DateTimeField("返却日時", blank=True, null=True)
    memo = models.TextField("メモ", blank=True)

    class Meta:
        ordering = ["returned_at", "-loaned_at"]

    def __str__(self):
        return f"{self.item} - {self.borrower_name}"

    @property
    def is_overdue(self):
        return self.returned_at is None and self.due_date < timezone.localdate()

