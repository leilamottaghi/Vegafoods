
from django.urls import path
from .views import RegistrationView, LoginView, LogoutView ,UserProfileView,EditUserProfileView,EditUserAddressView
from .views import *
app_name = 'accounts'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('edit_profile/', EditUserProfileView.as_view(), name='edit_profile'),
    path('edit_address/<int:address_id>/', EditUserAddressView.as_view(), name='edit_address'),
    path('create_address/', CreateAddressView.as_view(), name='create_address'),
    ]
