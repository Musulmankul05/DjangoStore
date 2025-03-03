import stripe
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView

from MusulmankulNew import settings
from MusulmankulNew.mixins import NotLogged404Mixin

from django.http import Http404, JsonResponse
from .forms import OrderForm
from .models import OrderModel
from store.models import BasketModel, ItemModel


# Create your views here.
class CheckoutView(CreateView):
    template_name = 'checkout.html'
    model = OrderModel
    form_class = OrderForm
    success_url = reverse_lazy('order_done')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("Вы не авторизованы!")

        baskets = BasketModel.objects.filter(user=request.user)
        if not baskets.exists():
            return redirect('store:catalog')

        return super(CheckoutView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            print("Form is valid.")
            order = form.save()
            if order:
                return redirect(self.success_url)
            else:
                print("Order was not saved.")
        else:
            print("Form is not valid.")
            print(form.errors)  # Print the form errors for debugging

        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = BasketModel.objects.filter(user=self.request.user)
        total = sum(basket.item.price * basket.quantity for basket in context['baskets'])
        context['total'] = total
        return context


class OrderItemsView(NotLogged404Mixin, TemplateView):
    template_name = 'order_items.html'
    message404 = 'Вы не авторизованы!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            items = OrderModel.objects.get(id=self.kwargs['order_id'], user=self.request.user)
        except OrderModel.DoesNotExist:
            raise Http404("У вас нету новых заказов")

        context = {"items": []}
        for i, j in items.items.items():
            item = {
                "id": i,
                "name": ItemModel.objects.get(id=i),
                "price": j["price"],
                "quantity": j["quantity"],
            }
            context['items'].append(item)
        context['total'] = items.price
        return context


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Lacoste black polo',
                        'quantity': 200,
                        'currency': 'som',
                        'amount': '200',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class OrderSuccessView(TemplateView):
    template_name = 'order_success.html'
