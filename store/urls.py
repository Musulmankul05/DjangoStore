from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path("remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path("categories/", cache_page(60)(views.CategoriesView.as_view()), name="categories"),
    path("categories/<slug:cat_slug>/", cache_page(60 * 5)(views.CategoriesByView.as_view()), name="categories_by"),
    path("catalog/<slug:tag_slug>/", cache_page(60 * 5)(views.GenByView.as_view()), name="tag_by"),
    path("items/<int:item_id>/", views.ItemPageView.as_view(), name="item"),
]
