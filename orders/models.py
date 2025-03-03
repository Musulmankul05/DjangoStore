from django.db import models
from random import randint

from users.models import UserModel


# Create your models here.
class OrderModel(models.Model):
    PROCESSING = 'processing'
    ON_THE_WAY = 'on_the_way'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

    ORDER_STATUS_CHOICES = [
        (PROCESSING, 'Подготовка заказа'),
        (ON_THE_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
        (CANCELED, 'Отменен'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=36, decimal_places=2)
    items = models.JSONField(default=dict)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default=PROCESSING)
    code = models.CharField(max_length=7, unique=True)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_order_code(self):
        while True:
            code = f"{randint(100000000, 999999999):09d}"
            if not OrderModel.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_order_code()
        super(OrderModel, self).save(*args, **kwargs)

    def __str__(self):
        return f'Заказ {self.user.username}: {self.price} | {self.created_at:%Y/%m/%d %H:%M}'

    class Meta:
        verbose_name = 'модель заказа'
        verbose_name_plural = 'заказы'
