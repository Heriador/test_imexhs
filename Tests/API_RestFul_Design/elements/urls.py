from django.urls import path, include
from rest_framework import routers
from .views import element_list, element_detail

router = routers.DefaultRouter()


urlpatterns = [
    path("elements/", element_list),
    path("elements/<str:pk>/", element_detail),
]
