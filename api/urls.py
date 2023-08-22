
from django.contrib import admin
from django.urls import path, include
from moviemixer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('api/get_random_movie/', get_random_movie, name="get_random_movie"),
    path('api/get_trailers/', get_trailers, name = "get_trailers"),

]

# Add to the bottom of the urls.py in the project directory.

from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)