from django.urls import path
from users.views import get_token, signup

urlpatterns = [
    path('signup/', signup),
    path('token/', get_token),
]
