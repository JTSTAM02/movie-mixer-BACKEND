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

def get_trailers(request):
            id = request.GET.get("id")
            url = "https://moviesdatabase.p.rapidapi.com/titles/random"
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
    

 



def get_filtered_random_movie(request):
    try:
        user_answers = request.GET.getlist("answers[]", [])

        # Set up headers for API request
        headers = {
            "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
        }

        # Build query parameters based on user answers
        query_params = {
            "mood": user_answers[1] if len(user_answers) > 1 else None,
            "genre": user_answers[2] if len(user_answers) > 2 else None,
            "decade": user_answers[3] if len(user_answers) > 3 else None,
            "duration": user_answers[4] if len(user_answers) > 4 else None,
            "rating": user_answers[5] if len(user_answers) > 5 else None,
            "special_awards": user_answers[6] if len(user_answers) > 6 else None,
            # Add more query parameters based on the user's other answers
        }

        response = requests.get(
            "https://moviesdatabase.p.rapidapi.com/titles/",
            headers=headers,
            params=query_params
        )

        movie_data = response.json()

        # Return the movie_data response or process it further as needed
        return JsonResponse(movie_data)
        
    except requests.RequestException as e:
        return JsonResponse({"error": "Error fetching filtered random movie"}, status=500)







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
    

def filter_movies(request):
    genre = request.GET.get("genre")
    title_type = request.GET.get("titleType")
    start_year = request.GET.get("startYear")
    end_year = request.GET.get("endYear")

    # Construct URL with query parameters
    url = "https://moviesdatabase.p.rapidapi.com/titles"
    headers = {
        'X-RapidAPI-Key': 'ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b',
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
    }
    params = {
        "genre": genre,
        "titleType": title_type,
        "startYear": start_year,
        "endYear": end_year,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        movies_data = response.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Failed to fetch movies from API: {str(e)}"}, status=500)

    # Apply filtering to the fetched data
    filtered_movies = []
    for movie_data in movies_data.get("results", []):
        if (
            (not genre or genre in movie_data.get("genres", []))
            and (not title_type or title_type == movie_data.get("titleType", ""))
            and (not start_year or int(start_year) <= int(movie_data.get("releaseYear", 0)))
            and (not end_year or int(end_year) >= int(movie_data.get("releaseYear", 0)))
        ):
            filtered_movies.append({"title": movie_data.get("titleText", "")})

    return JsonResponse(filtered_movies, safe=False)

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





class MovieViewSet(viewsets.ModelViewSet):
    queryset = movie.objects.all()
    serializer_class = movieSerializer