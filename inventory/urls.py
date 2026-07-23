from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("items/new/", views.item_create, name="item_create"),
    path("loans/", views.loan_list, name="loan_list"),
    path("loans/new/", views.loan_create, name="loan_create"),
    path("loans/<int:pk>/return/", views.return_loan, name="return_loan"),
]

