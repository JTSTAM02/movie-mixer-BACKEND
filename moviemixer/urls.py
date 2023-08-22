from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
# router.register(r'movies', MovieViewSet)


urlpatterns = [
    # API URLs from the router
    path('', include(router.urls)),
    path('get_random_movie/', get_random_movie, name='get_random_movie'),
    path('get_trailers/<int:id>/', get_trailers, name='get_trailers'),
    path('user/login/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


    