from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register')
]