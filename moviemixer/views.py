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
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated




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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    serializer = WatchlistSerializer(watchlist, many=True)
    return Response({'watchlist': serializer.data})


# @api_view(['POST'])
# def add_movie(request):
#     if request.method == 'POST':
#         movie_data = JSONParser().parse(request)
#         movie_serializer = movieSerializer(data=movie_data)
#         if movieSerializer.is_valid():
#             movieSerializer.save()
#         return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)
#     return Response(movie_serializer.errors, status=400)


@api_view(['POST'])
def add_movie(request):
    if request.method == 'POST':
        movie_data = request.data  # Get the movie data from the request
        movie_serializer = movieSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            user = request.user
            movie_id = movie_data['id']  # Assuming the movie id is included in the request data
            movie_instance = Movie.objects.get(id=movie_id)
            Watchlist.objects.create(user=user, movie=movie_instance)
            return Response({'message': 'Movie added to watchlist'}, status=status.HTTP_201_CREATED)
        return Response(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def add_watchlist_movie(request):
    user = request.user
    movie_data = {
            "title": request.data.get("title"),
            "release_year": request.data.get("release_year"),
            "description": request.data.get("description"),
            "image": request.data.get("image"),
            "userRating": request.data.get("userRating"),
            "trailerLink": request.data.get("trailerLink"),
        }

    try:
        movie = Movie.objects.get(id=movie_data["title"]) # getting the movie from the db if it exists, 3rd party api
    except Movie.DoesNotExist:
       
        movie = Movie.objects.create(**movie_data)
    added_at = request.data.get("added_at")
    watchlist_data = Watchlist.objects.create(user=user, movie=movie, added_at = added_at)
    watchlist_data.save()
    message = 'Game added to favorites'
    response_status = status.HTTP_201_CREATED
        
    return Response({'message':message}, status=response_status)


