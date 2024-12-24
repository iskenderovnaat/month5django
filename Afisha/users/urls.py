from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.registration_api_view, name='registration'),
    path('authorization/', views.authorization_api_view, name='authorizations'),
    path('confirm/', views.confirm_user_api_view, name='confirm_user'),

]