from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    # API URLs from the router
    path('api/', include(router.urls)),
    path('api/get_random_movie/', get_random_movie, name="get_random_movie"),
    path("movie_filter/", MovieFilterView.as_view(), name="movie_filter"),
    path('api/get_all_movies/', get_all_movies, name="get_all_movies"),
    path('api/filter_movies/', filter_movies, name="filter_movies")
    ]

