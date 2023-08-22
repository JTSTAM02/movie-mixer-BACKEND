from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    # API URLs from the router
    path('api/', include(router.urls)),
    path('api/get_random_movie/', get_random_movie, name="get_random_movie"),
    path('api/get_trailers/', get_trailers, name = "get_trailers"),
    ]

