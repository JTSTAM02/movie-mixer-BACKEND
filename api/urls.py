
from django.contrib import admin
from django.urls import path, include
from moviemixer.views import get_random_movie, MovieFilterView, get_recommendations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('api/get_random_movie/', get_random_movie, name="get_random_movie"),
    path("movie-filter/", MovieFilterView.as_view(), name="movie_filter"),
    path('api/get_recommendations/', get_recommendations, name="get_recommendations"),
]

# Add to the bottom of the urls.py in the project directory.

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)