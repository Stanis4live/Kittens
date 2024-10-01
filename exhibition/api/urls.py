from django.urls import path, include

urlpatterns = [
    path('v1/user/', include('exhibition.api.v1.urls')),
]