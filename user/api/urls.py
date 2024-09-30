from django.urls import path, include

urlpatterns = [
    path('v1/user/', include('user.api.v1.urls')),
]