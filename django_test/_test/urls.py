from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import auth_logout
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('logout', auth_logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('', views.index, name='test'),
    path('add_cat', views.add_category),
    path('del_cat', views.del_category),
    path('go_to', views.go_to),
    path('add_file', views.add_file),
    path('del_file', views.del_file),
    path('get_files', views.get_files),
]
