from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
# router.register(r'user', UserViewSet)



urlpatterns = [
    # API URLs from the router
    path('', include(router.urls)),
    path('get_random_movie/', get_random_movie, name='get_random_movie'),
    path('get_top_movies/', getTopMovies, name='get_top_movies'),
    path('get_trailers/<str:id>/', get_trailers, name='get_trailers'),
    path('user/signup/', UserCreate.as_view(), name="create_user"),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/<int:pk>/', UserDetail.as_view(), name='get_user_details'), 
    path('add_to_watchlist/', add_to_watchlist, name='add_to_watchlist'), 
    path('get_watchlist/', get_watchlist, name='get_watchlist'),
    path('add_movie/', add_movie, name='add_movie'),


]

