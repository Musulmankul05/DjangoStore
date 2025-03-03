from django.contrib import admin

from orders.models import OrderModel


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'created_at', ]
    fields = (('user', 'full_name',), 'price', 'created_at', 'code', 'address', 'status', 'items',)
    readonly_fields = ('created_at', 'code', 'address',)
