from datetime import datetime

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from translator.translator import Translator
import secrets
import requests

from MusulmankulNew import settings

API = {'country_code': 'https://api.first.org/data/v1/countries/?q={country}', }


def calculate_age(birthdate):
    try:
        today = datetime.now().date()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if birthdate.month == 2 and birthdate.day == 29:
            try:
                leap_year_birthday = birthdate.replace(year=today.year)
            except ValueError:
                leap_year_birthday = birthdate.replace(year=today.year, day=28)
            if today < leap_year_birthday:
                age -= 1
        return age
    except AttributeError:
        return


def translator_func(text: str, en_ru: bool = True) -> str:
    if not en_ru:
        translator = Translator(from_lang='ru', to_lang='en')
    translator = Translator(from_lang='en', to_lang='ru')
    translation = translator.translate(text)
    return translation.text


def get_country_code(country_name: str):
    api = API['country_code']
    try:
        response = requests.get(api.format(country=country_name.lower()))
        response_json = response.json()
        code = response_json['data'].keys()
        return ''.join([i for i in code])
    except requests.exceptions.ConnectionError as e:
        return False


def current_page(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def send_verification(email, token):
    confirmation_link = 'http://127.0.0.1:8000' + reverse('users:confirm_email', args=[token])
    subject = 'Подтверждение электронной почты'
    message = f'Пожалуйста, подтвердите свою электронную почту, перейдя по следующей ссылке: {confirmation_link}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])


def generate_token():
    return secrets.token_urlsafe(16)
