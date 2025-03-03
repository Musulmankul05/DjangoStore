from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.utils.timezone import now
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView

from orders.models import OrderModel
from .models import *
from .forms import *

from MusulmankulNew import functions


class ProfileView(TemplateView):
    template_name = "profile.html"
    country = 'Kyrgyzstan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['age'] = functions.calculate_age(user.date_birth)
        context['country'] = self.country
        context['orders'] = OrderModel.objects.filter(user=self.request.user)
        context['country_code'] = functions.get_country_code(self.country)
        return context


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    model = UserModel
    form_class = LoginForm
    success_url = reverse_lazy('store:index')


class UserRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    model = UserModel
    form_class = RegisterForm
    success_url = reverse_lazy('users:send_confirmation_email')


@login_required
def profile_update(request, username):
    if request.method == 'POST':
        form = EditProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = EditProfileForm(instance=request.user)
    context = {'form': form}
    return render(request, 'edit.html', context)


def send_confirmation_email(request):
    user = request.user
    expiration = now() + timedelta(hours=12)
    verifier = EmailVerificationModel.objects.create(user=user, expires=expiration, code=functions.generate_token())
    verifier.send_verification_email()
    return render(request, 'email_verification.html',
                  {'message': f'Ссылка с подтверждением вашей электронной почты {user.email} отправлена\n'
                              'Ссылка будет работать в течении 12 часов'})


class EmailVerificationView(TemplateView):
    template_name = 'email_verification.html'


def confirm_email(request, token):
    confirmation_token = get_object_or_404(EmailVerificationModel, code=token)
    if confirmation_token.is_expired():
        return render(request, 'email_verification.html', {'message': 'Срок действия ссылки подтверждения истек.'})

    user = confirmation_token.user
    user.email_verified = True  # Или любое другое действие, например подтверждение email
    user.save()

    confirmation_token.delete()

    return render(request, 'email_verification.html', {'message': 'Ваша электронная почта успешно подтверждена.'})


def user_logout(request):
    auth.logout(request)
    return redirect('store:index')
