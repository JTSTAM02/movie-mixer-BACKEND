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
from rest_framework.decorators import action
from datetime import date



def get_random_movie_family_friendly(request):
    try:
        genre = request.GET.get('genre')
        startYear = request.GET.get('startYear')
        endYear = request.GET.get('endYear')

        url = "https://moviesdatabase.p.rapidapi.com/titles/random"

        querystring = {
            "list": "most_pop_movies",
            "genre": "Family",
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def get_watchlist(request):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    serializer = WatchlistSerializer(watchlist, many=True)
    return Response({'watchlist': serializer.data})


# @api_view(['POST'])
# def add_movie_and_watchlist(request):
#     if request.method == 'POST':
#         user=request.user
#         alphabetic_id = request.data.get("alphabetic_id")
#         movie_data = request.data  # Get the movie data from the request
#         movie_id = 0
#         movie = Movie.objects.filter(alphabetic_id__exact=alphabetic_id).first()
#         if not movie:
#             movie_serializer = movieSerializer(data=movie_data)
#             if movie_serializer.is_valid():
#             # Save the movie instance and retrieve the saved instance with the generated ID
#                 movie_instance = movie_serializer.save()             
#                 movie_id = movie_instance.id
#         else:
#             movie_id = movie.id
        

#         watchlist_data = {
#             'user': user.id,
#             'movie': movie_id,
#             'added_at': date.today()  # Use movie's release year or other appropriate data
#         }
#         watchlist = Watchlist.objects.filter(movie=movie_id, user=user)
#         if not watchlist:
#             watchlist_serializer = WatchlistSerializer(data=watchlist_data)
#             if watchlist_serializer.is_valid():
#                 watchlist_serializer.save()

#                 response_data = {
#                     'message': 'Movie added to watchlist',
#                     'movie': movie_serializer.data,  # Include the serialized movie object
#                     'watchlist': watchlist_serializer.data  # Include the serialized watchlist entry
#                 }

#                 return Response(response_data, status=status.HTTP_201_CREATED)
#                 # return Response({'message': 'Movie added to watchlist'}, status=status.HTTP_201_CREATED)
#             return Response(watchlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'message': 'Movie already in watchlist'}, status=status.HTTP_200_OK)

#     return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)





@api_view(['POST'])
def add_movie_and_watchlist(request):
    if request.method == 'POST':
        user = request.user
        alphabetic_id = request.data.get("alphabetic_id")
        movie_data = request.data  # Get the movie data from the request
        movie_id = 0
        movie_instance = None  # Initialize movie_instance

        movie = Movie.objects.filter(alphabetic_id__exact=alphabetic_id).first()
        if not movie:
            movie_serializer = movieSerializer(data=movie_data)
            if movie_serializer.is_valid():
                # Save the movie instance and retrieve the saved instance with the generated ID
                movie_instance = movie_serializer.save()
                movie_id = movie_instance.id
        else:
            movie_id = movie.id

        # Check if movie_instance is not None before using it
        if movie_instance:
            movie_serializer = movieSerializer(movie_instance)  # Pass the movie instance

        watchlist_data = {
            'user': user.id,
            'movie': movie_id,
            'added_at': date.today()  # Use movie's release year or other appropriate data
        }
        
        watchlist = Watchlist.objects.filter(movie=movie_id, user=user)
        if not watchlist:
            watchlist_serializer = WatchlistSerializer(data=watchlist_data)
            if watchlist_serializer.is_valid():
                watchlist_instance = watchlist_serializer.save()
                watchlist_id = watchlist_instance.id

                response_data = {
                    'message': 'Movie added to watchlist',
                    'movie': movie_serializer.data if movie_instance else None,  # Include the serialized movie object if available
                    'watchlist': watchlist_serializer.data
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            return Response(watchlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Movie already in watchlist'}, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)






class MovieCreateSet(viewsets.ModelViewSet):
     queryset= Movie.objects.all()
     serializer_class = movieSerializer


class WatchlistViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def add_to_watchlist(self, request):
        user = request.user
        movie_id = request.data.get("movie_id")

        try:
            movie = Movie.objects.get(alphabetic_id=movie_id)
        except Movie.DoesNotExist:
            # return Response({"message": "Movie not found"}, status=404)

            watchlist_entry, created = Watchlist.objects.get_or_create(user=user, movie=movie)

        if created:
            message = 'Movie added to watchlist'
            status_code = 201
        else:
            watchlist_entry.delete()
            message = 'Movie removed from watchlist'
            status_code = 200

        return Response({"message": message}, status=status_code)
    




@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_movie(request):
    user = request.user
    movie_data = Movie.objects.filter(user=user)
    serializer = movieSerializer(movie_data, many=True)
    return Response({'movie data': serializer.data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_watchlist(request, movie_id):
    user = request.user

    try:
        watchlist_item = Watchlist.objects.get(user=user, movie=movie_id)
        watchlist_item.delete()
        return Response({'message': 'Movie removed from watchlist'}, status=status.HTTP_200_OK)
    except Watchlist.DoesNotExist:
        return Response({'message': 'Movie not found in watchlist'}, status=status.HTTP_404_NOT_FOUND)