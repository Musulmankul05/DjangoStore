from django import template
from random import randint

register = template.Library()


@register.filter(name='randomprice')
def random_price(value):
    return value + str(float(str(randint(1, 100))
                             + '.' + str(randint(1, 100))))
