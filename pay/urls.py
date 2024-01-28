from django.urls import path
from .views import *

urlpatterns = [
    path("", InitializePayment.as_view(), name="initialize-payment"),
    path("verify-payment/", VerifyPaymentView.as_view(), name="verify-payment"),
]
