from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ItemForm, LoanForm
from .models import Item, Loan


def dashboard(request):
    keyword = request.GET.get("q", "").strip()
    items = Item.objects.all()
    if keyword:
        items = items.filter(Q(name__icontains=keyword) | Q(category__icontains=keyword) | Q(location__icontains=keyword))
    active_loans = Loan.objects.filter(returned_at__isnull=True).select_related("item")
    context = {
        "items": items,
        "keyword": keyword,
        "active_loans": active_loans[:5],
        "item_count": Item.objects.count(),
        "loan_count": active_loans.count(),
        "low_stock_count": sum(item.available_quantity <= 1 for item in Item.objects.all()),
    }
    return render(request, "inventory/dashboard.html", context)


def item_create(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "備品を登録しました。")
        return redirect("dashboard")
    return render(request, "inventory/form.html", {"form": form, "title": "備品を登録"})


def loan_create(request):
    form = LoanForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "貸出を登録しました。")
        return redirect("loan_list")
    return render(request, "inventory/form.html", {"form": form, "title": "貸出を登録"})


def loan_list(request):
    loans = Loan.objects.select_related("item")
    return render(request, "inventory/loan_list.html", {"loans": loans})


def return_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk, returned_at__isnull=True)
    if request.method == "POST":
        loan.returned_at = timezone.now()
        loan.save(update_fields=["returned_at"])
        messages.success(request, f"{loan.item.name} の返却を登録しました。")
    return redirect("loan_list")

