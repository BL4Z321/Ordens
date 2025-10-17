from django.shortcuts import redirect
from django.urls import reverse


class RestrictAminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')):
            user = request.user
            if not user.is_authenticated or not hasattr(user, 'usuario') or user.usuario.role != 'admin':
                return redirect('login')
        return self.get_response(request)