
from django.contrib import admin
from django.urls import path, include
from moviemixer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('api/get_random_movie/', get_random_movie, name="get_random_movie"),
    path("movie_filter/", MovieFilterView.as_view(), name="movie_filter"),
    path('api/get_all_movies/', get_all_movies, name="get_all_movies"),
    path('api/filter_movies/', filter_movies, name="filter_movies"),
    path('api/get-filtered-random-movies/', get_filtered_random_movie)
]

# Add to the bottom of the urls.py in the project directory.

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)