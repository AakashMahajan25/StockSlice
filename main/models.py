from django.db import models
from base.models import BaseModel
from accounts.models import Profile

class StockTransaction(BaseModel):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='stock_transactions')
    stock_name = models.CharField(max_length=255)
    bought_at_value = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    is_sold = models.BooleanField(default=False)
    sold_at_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.stock_name} - Quantity: {self.quantity}"