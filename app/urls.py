from django.urls import path
from app import auth
from app.auth import LoginUser

urlpatterns = [
    path('login', LoginUser.as_view(), name='login'),
    path('logout/', auth.logout_view, name='logout'),

]