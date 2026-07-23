from django import forms
from django.utils import timezone

from .models import Item, Loan


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "category", "total_quantity", "location", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["item", "borrower_name", "due_date", "memo"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "memo": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["item"].queryset = Item.objects.all()
        self.fields["due_date"].initial = timezone.localdate() + timezone.timedelta(days=7)

    def clean_item(self):
        item = self.cleaned_data["item"]
        if item.available_quantity < 1:
            raise forms.ValidationError("この備品はすべて貸出中です。")
        return item

