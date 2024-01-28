from .serializers import PaymentSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
import requests
from django.db import transaction

from .models import Payment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class InitializePayment(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def get(self, request):
        return Response({"message": "Hello GET"}, status=status.HTTP_200_OK)

    def post(self, request):
        transaction_url = f"{settings.PAYSTACK_URL}charge"
        secret_key = settings.PAYSTACK_SECRET_KEY

        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
        }

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            instance = serializer.save()
            data = {
                "email": instance.email,
                "amount": instance.amount_value(),
                "mobile_money": {
                    "phone" : "0245418403",
                    "provider" : "mtn"
                },
                "currency": "GHS",
                "reference": instance.ref,
            }
            response = requests.post(transaction_url, headers=headers, json=data)
            response_data = response.json()

            if response.status_code == status.HTTP_200_OK:
                
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                self.handle_external_request_failure(instance)
                return Response(
                    {response_data["message"]}, status=status.HTTP_400_BAD_REQUEST
                )

        except requests.RequestException as e:
            self.handle_external_request_failure(instance)
            return Response(
                {"message": f"Network error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def handle_external_request_failure(self, instance):
        if instance and instance.id:
            print(
                "Deleting instance:",
                instance.email,
                instance.amount,
                instance.channel,
                instance.ref,
            )
            instance.delete()


class VerifyPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        reference = request.data.get("reference")

        if reference:
            response = PaystackService.verify_payment(reference)
            return Response(response)

        return Response(
            {"message": "Invalid or missing reference"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PaystackService:
    @staticmethod
    def verify_payment(reference):
        url = f"{settings.PAYSTACK_URL}transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        return response.json()
