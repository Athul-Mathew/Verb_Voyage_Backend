import json
from rest_framework import generics
from django.utils import timezone

import stripe
from django.conf import settings
import logging
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from .serializers import SubscriptionPlanSerializer
from .models import SubscriptionPlan
logger = logging.getLogger(__name__)
from django.shortcuts import get_object_or_404, render
from django.views import View
from .import client
from rest_framework.serializers import ValidationError


from .serializers import *
from rest_framework.decorators import api_view




import razorpay
# Create your views here.
class SubscriptionPlanList(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class SubscriptionPlanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class RazorpayClient:

    def create_order(self,amount,currency):
        data = {
            "amount" : amount * 100,
            "currency" : currency,
        }
        try:
            order_data = client.order.create(data=data)
            return order_data
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )
    
    def verify_payment(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            return client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except Exception as e:
            raise ValidationError(
                {
                    "status_code" : status.HTTP_400_BAD_REQUEST,
                    "message" : e
                }
            )


rz_client = RazorpayClient


class CreateOrderAPIView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(UserAccount, id=user_id)
        create_order_serializer = CreateOrderSerializer(data=request.data)
        if create_order_serializer.is_valid():
            rz_client_instance = RazorpayClient()  
            order_response = rz_client_instance.create_order(
                amount=create_order_serializer.validated_data.get("amount"),
                currency=create_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": create_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def TransactionAPIView(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(UserAccount, id=user_id)
        duration = request.data.get("duration")
        print("Request Data:", request.data)

        if duration is not None:
          
            print("Duration:", duration)

            
            user.remaining_subscription_days = duration

        else:
           
            print("Duration is missing or None")

        transaction_serializer = TransactionModelSerializer(data=request.data)

        if transaction_serializer.is_valid():
            rz_client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

            try:
                rz_client.utility.verify_payment_signature({
                    "razorpay_signature": transaction_serializer.validated_data.get("signature"),
                    "razorpay_payment_id": transaction_serializer.validated_data.get("payment_id"),
                    "razorpay_order_id": transaction_serializer.validated_data.get("order_id"),
                })
            except Exception as e:
                return JsonResponse({
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "bad request",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            # Save the transaction
            transaction = transaction_serializer.save(user=user)

            # Update user status and remaining days
            user.is_premium = True
            user.save()  # Save the user object with updated premium status and remaining days
            
            return JsonResponse({
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction created"
            }, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)
