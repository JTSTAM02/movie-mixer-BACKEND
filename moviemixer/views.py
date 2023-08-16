from django.shortcuts import render
import requests
from rest_framework import viewsets
from .models import movie
from .serializers import movieSerializer
import random
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import movie

def get_recommendations(answers):
    genre = answers.get("genre")
    decade = answers.get("decade")
    actors = answers.get("actors")
    directors = answers.get("directors")
    duration = answers.get("duration")
    mood = answers.get("mood")
    rating = answers.get("rating")

    # Build a query based on the selected answers
    query = movie.objects.all()  # Replace 'Movie' with your actual model name
    if genre:
        query = query.filter(genre=genre)
    if decade:
        query = query.filter(decade=decade)
    if actors:
        query = query.filter(actors__icontains=actors)
    if directors:
        query = query.filter(directors__icontains=directors)
    if duration:
        query = query.filter(duration=duration)
    if mood:
        query = query.filter(mood=mood)
    if rating:
        query = query.filter(rating=rating)

    # Return recommended movies as a list of dictionaries
    recommended_movies = [{"title": movie.title} for movie in query]
    return recommended_movies

def get_movie_recommendations(request):
    recommended_movies = get_recommendations(request.query_params)

    return JsonResponse(recommended_movies, safe=False)



class MovieFilterView(APIView):
    def post(self, request, *args, **kwargs):
        selected_genre = request.data.get("selected_genre")
        # Implement logic to filter movies based on selected_genre
        # For now, let's assume the filtered movies are fetched from the backend
        filtered_movies = [
            { "title": "Movie 1", "genre": "Action" },
            { "title": "Movie 2", "genre": "Comedy" },
            # Add more movies
        ]
        return Response({"filtered_movies": filtered_movies}, status=status.HTTP_200_OK)


def get_random_movie(request):
    try:
        response = requests.get(
            "https://moviesdatabase.p.rapidapi.com/titles/",
            headers={
	        "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
	        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            },
        )
        movie_data = response.json()
        return JsonResponse(movie_data)
    except requests.RequestException as e:
        return JsonResponse({"error": "Error fetching random movie"}, status=500)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = movie.objects.all()
    serializer_class = movieSerializer