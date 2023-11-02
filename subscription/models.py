
from django.db import models
from datetime import datetime, timedelta
from  Accounts.models import UserAccount     

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    desc=models.CharField(max_length=100,default='NONE')
    edit_url = models.URLField(blank=True ,null=True)  

    def __str__(self):
        return self.name




class Subscription(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.now)
    duration = models.IntegerField(default=30)  # Default to 30 days

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration)


class Transaction(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID")
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    signature = models.CharField(max_length=200, verbose_name="Signature")
    amount = models.IntegerField(verbose_name="Amount")
    datetime = models.DateTimeField(auto_now_add=True)
    duration=models.IntegerField(default=0)

    def _str_(self) -> str:
        return str(self.id)