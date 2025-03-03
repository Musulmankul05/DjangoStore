from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import ItemModel, BasketModel, CategoryModel, TagModel
from MusulmankulNew.functions import current_page


class IndexView(TemplateView):
    template_name = "index.html"


class CatalogView(ListView):
    template_name = "catalog.html"
    model = ItemModel
    paginate_by = 8
    context_object_name = 'object_list'

    def get_queryset(self):
        sort_by = self.request.GET.get("sort", )
        if sort_by == "asc":
            return ItemModel.objects.all().order_by("price")
        elif sort_by == "desc":
            return ItemModel.objects.all().order_by("-price")
        else:
            return ItemModel.objects.all().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort", )
        return context


class CategoriesView(TemplateView):
    template_name = 'categories.html'


class CategoriesByView(ListView):
    template_name = 'cat_by.html'
    model = ItemModel
    paginate_by = 8
    context_object_name = 'object_list'

    def get_queryset(self):
        slug = self.kwargs["cat_slug"]
        sort_by = self.request.GET.get("sort", )
        queryset = ItemModel.objects.filter(category__slug=slug).select_related("category")
        if sort_by == "asc":
            return queryset.order_by("price")
        elif sort_by == "desc":
            return queryset.order_by("-price")
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(CategoryModel, slug=self.kwargs['cat_slug'])
        context["sort_by"] = self.request.GET.get("sort", )
        return context


class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    model = BasketModel

    def get_queryset(self):
        return BasketModel.objects.filter(user=self.request.user).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = sum(basket.item.price * basket.quantity for basket in context['object_list'])
        context['total'] = total
        return context


class GenByView(ListView):
    template_name = 'cat_by.html'
    model = ItemModel
    paginate_by = 8
    context_object_name = 'object_list'

    def get_queryset(self):
        tag = self.kwargs["tag_slug"]
        sort_by = self.request.GET.get("sort", )
        queryset = ItemModel.objects.filter(tags__slug=tag)
        if sort_by == "asc":
            return queryset.order_by("price")
        elif sort_by == "desc":
            return queryset.order_by("-price")
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = TagModel.objects.get(slug=self.kwargs['tag_slug'])
        context["sort_by"] = self.request.GET.get("sort", )
        return context


class ItemPageView(TemplateView):
    template_name = 'item_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['item'] = ItemModel.objects.get(id=self.kwargs['item_id'])
        return context


def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('/signin/')

    item = ItemModel.objects.get(id=item_id)
    cart = BasketModel.objects.filter(user=request.user, item=item)

    if item.quantity <= 0:
        raise Http404("Неверный запрос")

    if not cart.exists():
        BasketModel.objects.create(user=request.user, item=item, quantity=1)
        return current_page(request)
    else:
        basket = cart.first()
        basket.quantity += 1
        basket.save()
        return current_page(request)


def remove_from_cart(request, id):
    cart = BasketModel.objects.filter(id=id)
    if cart.exists():
        basket = cart.first()
        if basket.quantity > 1:
            basket.quantity -= 1
            basket.save()
        else:
            basket.delete()
    return current_page(request)
