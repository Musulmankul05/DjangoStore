from django.urls import path

from orders import views

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('success/', views.OrderSuccessView.as_view(), name='order_done'),
    path('<int:order_id>/', views.OrderItemsView.as_view(), name='order_list'),
    path('config/', views.stripe_config, name='stripe_config'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]
