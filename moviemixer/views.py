import requests
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status



def get_random_movie(request):
    try:
        genre = request.GET.get('genre')
        startYear = request.GET.get('startYear')
        endYear = request.GET.get('endYear')

        url = "https://moviesdatabase.p.rapidapi.com/titles/random"

        querystring = {
            "list": "most_pop_movies",
            "genre": genre,
            "info": "base_info",
            "startYear": startYear,
            "endYear": endYear,
        }

        headers = {
            "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        movie_data = response.json()
        return JsonResponse(movie_data)
    except requests.RequestException as e:
        return JsonResponse({"error": "Error fetching random movie"}, status=500)

def get_trailers(request, id):
            url = f"https://moviesdatabase.p.rapidapi.com/titles/{id}"
            querystring = {
                "list": "most_pop_movies",
                "info": "trailer"
            }

            headers = {
            "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            movie_data = response.json()
            return JsonResponse(movie_data)


def getTopMovies(request):
            url = "https://moviesdatabase.p.rapidapi.com/titles/"
            querystring = {
                "list": "top_boxoffice_200",
                "info": "base_info",

            }
            response = requests.get(url)
            headers = {
            "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            movie_data = response.json()
            return JsonResponse(movie_data)
    


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = movieSerializer


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer


@api_view(['POST'])
def add_to_watchlist(request):
    if request.method == 'POST':
        watchlist_data = JSONParser().parse(request)
        watchlist_serializer = WatchlistSerializer(data=watchlist_data)
        if watchlist_serializer.is_valid():
             watchlist_serializer.save()
        return JsonResponse(watchlist_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(watchlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)