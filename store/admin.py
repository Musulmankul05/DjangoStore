from django.contrib import admin
from .models import *


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "slug",
        "description",
    )
    list_display = (
        "name",
        "slug",
        "description",
    )


@admin.register(ItemModel)
class ItemAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "price",
        "category",
        "quantity",
        "description",
        "image",
    )
    list_display = (
        "name",
        "price",
        "category",
        "quantity",
        "description",
        "image",
    )


admin.site.register(BasketModel)
admin.site.register(TagModel)
