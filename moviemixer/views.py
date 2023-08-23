import requests
from rest_framework import viewsets
from .models import movie
from .serializers import movieSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import movie
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework.decorators import action
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import *
from .serializers import *
from django.db.models import Sum




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




# -------------------Working Function------------------------------
# def get_random_movie(request):
#     try:
#         genre = request.GET.get('genre')
#         startYear = request.GET.get('startYear')
#         endYear = request.GET.get('endYear')

#         url = "https://moviesdatabase.p.rapidapi.com/titles/random"

#         querystring = {"list":"most_pop_movies", "genre": genre, "info": "base_info", "startYear": startYear, "endYear": endYear}

#         headers = {
#             "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
#             "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
#             }

#         response = requests.get(url, headers=headers, params=querystring)

#         movie_data = response.json()
#         return JsonResponse(movie_data)
    

    # except requests.RequestException as e:
        # return JsonResponse({"error": "Error fetching random movie"}, status=500)
    



# class UserLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(request, username=email, password=password)
#         if user:
#             login(request, user)
#             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class MovieViewSet(viewsets.ModelViewSet):
    queryset = movie.objects.all()
    serializer_class = movieSerializer


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny)
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
