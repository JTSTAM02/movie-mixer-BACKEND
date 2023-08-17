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

def get_all_movies(request):
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    headers = {
	    "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
	    "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({"error": "Failed to fetch movies"}, status=500)
    
import requests

def filter_movies(request):
    genre = request.GET.get("genre")
    title_type = request.GET.get("titleType")
    start_year = request.GET.get("startYear")
    end_year = request.GET.get("endYear")

    # Fetch movie data from the API
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    headers = {
        'X-RapidAPI-Key': 'ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b',
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch movies from API"}, status=500)
    
    movies_data = response.json()

    # Apply filtering to the fetched data
    filtered_movies = []
    for movie_data in movies_data["results"]:
        if (
            (not genre or genre in movie_data["genres"])
            and (not title_type or title_type == movie_data["titleType"])
            and (not start_year or int(start_year) <= int(movie_data["releaseYear"]))
            and (not end_year or int(end_year) >= int(movie_data["releaseYear"]))
        ):
            filtered_movies.append({"title": movie_data["titleText"]})

    return JsonResponse(filtered_movies, safe=False)

# def filter_movies(request):
#     genre = request.GET.get("genre")
#     title_type = request.GET.get("titleType")
#     start_year = request.GET.get("startYear")
#     end_year = request.GET.get("endYear")

#     query = movie.objects.all()

#     if genre:
#         query = query.filter(genre=genre)
#     if title_type:
#         query = query.filter(title_type=title_type)
#     if start_year:
#         query = query.filter(release_year__gte=start_year)
#     if end_year:
#         query = query.filter(release_year__lte=end_year)

#     filtered_movies = [{"title": movie.title} for movie in query]
#     return JsonResponse(filtered_movies, safe=False)

    # genre = request.GET.get("genre")


    # query = movie.objects.all()
    # if genre:
    #     query = query.filter(genre=genre)

    # filtered_movies = [{"title": movie.title} for movie in query]
    # return JsonResponse(filtered_movies, safe=False)


# def get_recommendations(answers):
#     try:
#         genre = answers["genre"]
#         decade = answers["decade"]
#         actors = answers["actors"]
#         directors = answers["directors"]
#         duration = answers["duration"]
#         mood = answers["mood"]
#         rating = answers["rating"]
#     except KeyError:
#         pass

#     query = movie.objects.all()  
#     if genre:
#         query = query.filter(genre=genre)
#     if decade:
#         query = query.filter(decade=decade)
#     if actors:
#         query = query.filter(actors__icontains=actors)
#     if directors:
#         query = query.filter(directors__icontains=directors)
#     if duration:
#         query = query.filter(duration=duration)
#     if mood:
#         query = query.filter(mood=mood)
#     if rating:
#         query = query.filter(rating=rating)

#     # Return recommended movies as a list of dictionaries
#     recommended_movies = [{"title": movie.title} for movie in query]
#     return recommended_movies

# def get_movie_recommendations(request):
#     recommended_movies = get_recommendations(request.query_params)
#     return JsonResponse(recommended_movies, safe=False)




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