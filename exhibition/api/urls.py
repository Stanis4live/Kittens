from django.urls import path, include

urlpatterns = [
    path('v1/exhibition/', include('exhibition.api.v1.urls')),
]