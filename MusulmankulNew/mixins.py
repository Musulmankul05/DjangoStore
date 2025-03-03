from django.http import Http404


class NotLogged404Mixin:
    message404 = 'You are not logged in!'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404(self.message404)
        return super().dispatch(request, *args, **kwargs)
