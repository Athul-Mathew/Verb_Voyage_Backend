from django.urls import path
from .views import  *
from . import views

urlpatterns = [
    path('subscription-plans/', SubscriptionPlanList.as_view(), name='subscription-plan-list'),
    path('subscription-plans/<int:pk>/', SubscriptionPlanDetail.as_view(), name='subscription-plan-detail'),
   
     path('subscription-plans/', SubscriptionPlanList.as_view(), name='subscription-plan-list'),
    
        # Use StripeCheckoutView directly
    # path('create-checkout-session/', views.create_checkout_session),
    # path('create-order/', views.create_order, name='create_order'),
 
    path("create/<int:user_id>/",CreateOrderAPIView.as_view(), name="create-order-api"),
    path("complete/<int:user_id>/",views.TransactionAPIView, name="complete-order-api"),


 
    
]
