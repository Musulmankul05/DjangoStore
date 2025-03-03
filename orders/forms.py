import json

from django import forms

from store.models import BasketModel, ItemModel
from .models import OrderModel


class OrderForm(forms.ModelForm):
    phone = forms.CharField(max_length=24, widget=forms.TextInput(
        attrs={'placeholder': '+996XXXXXXXXX', 'pattern': '^\+996\d{9}$', 'type': 'tel'}))

    class Meta:
        model = OrderModel
        fields = ('full_name', 'address', 'phone',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        print(self.user.id, self.user)
        if not self.user.phone:
            self.fields['phone'].required = True
        else:
            self.fields['phone'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        if not self.user.phone and self.user:
            self.user.phone = self.cleaned_data['phone']
            self.user.save()

        basket_items = BasketModel.objects.filter(user=self.user)
        items_data = {
            basket_item.item.id: {"price": str(basket_item.item.price), "quantity": str(basket_item.quantity)}
            for basket_item in basket_items}
        instance.items = items_data
        total = sum(basket.item.price * basket.quantity for basket in basket_items)
        instance.price = total
        instance.user = self.user
        for item in basket_items:
            record = ItemModel.objects.get(id=item.item.id)
            record.quantity -= item.quantity
            record.save()

        basket_items.delete()

        if commit:
            instance.save()

        return instance
