from django.contrib import admin

from .models import Item, Loan


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "total_quantity", "location")
    search_fields = ("name", "category")


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("item", "borrower_name", "due_date", "loaned_at", "returned_at")
    list_filter = ("returned_at", "due_date")

