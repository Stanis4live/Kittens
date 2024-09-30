from django.urls import path
from user.api.v1.views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
]