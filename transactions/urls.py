
from django.urls import path
from .views import DepositMoneyView

urlpatterns = [
    path('transactions/deposit/', DepositMoneyView.as_view(), name='deposit_money'),
]

