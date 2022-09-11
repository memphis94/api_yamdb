from django.urls import path

from users.views import signup, get_token

urlpatterns = [
    path('signup/', signup),
    path('token/', get_token),
]
