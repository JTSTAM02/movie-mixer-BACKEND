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

        url = "https://moviesdatabase.p.rapidapi.com/titles/random"

        querystring = {"list":"most_pop_movies", "genre": genre}

        headers = {
            "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
            }

        response = requests.get(url, headers=headers, params=querystring)

        movie_data = response.json()
        return JsonResponse(movie_data)

    except requests.RequestException as e:
        return JsonResponse({"error": "Error fetching random movie"}, status=500)
    

 

# def get_filtered_random_movie(request):
#     try:
#         user_answers = request.GET.getlist("answers[]", [])

#         # Set up headers for API request
#         headers = {
#             "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
#             "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
#         }

#         # Build query parameters based on user answers
#         query_params = {
#             "mood": user_answers[1],  # Based on the provided index in answers array
#             "genre": user_answers[2],  # Based on the provided index in answers array
#             "decade": user_answers[3],  # Based on the provided index in answers array
#             "duration": user_answers[4],  # Based on the provided index in answers array
#             "rating": user_answers[5],  # Based on the provided index in answers array
#             "special_awards": user_answers[6],  # Based on the provided index in answers array
#             # Add more query parameters based on the user's other answers
#         }

#         response = requests.get(
#             "https://moviesdatabase.p.rapidapi.com/titles/",
#             headers=headers,
#             params=query_params
#         )

#         movie_data = response.json()

#         # Return the movie_data response or process it further as needed
#         return JsonResponse(movie_data)
        
#     except requests.RequestException as e:
#         return JsonResponse({"error": "Error fetching filtered random movie"}, status=500)


import requests
from django.http import JsonResponse

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




# def get_filtered_random_movie(request):
#     try:
#         user_answers = request.GET.get("answers", [])  # Assuming you are sending answers as POST data

#         # Set up headers for API request
#         headers = {
#             "X-RapidAPI-Key": "ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b",
#             "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
#         }

#         # Build query parameters based on user answers
#         query_params = {
#             # Set your query parameters based on user answers, e.g. "genre": user_answers.get("genre")
#             # Make sure to match the parameter names with the API documentation
#         }

#         response = requests.get(
#             "https://moviesdatabase.p.rapidapi.com/titles/",
#             headers=headers,
#             params=query_params
#         )

#         movie_data = response.json()

#         # Return the movie_data response or process it further as needed
#         return JsonResponse(movie_data)
        
#     except requests.RequestException as e:
#         return JsonResponse({"error": "Error fetching filtered random movie"}, status=500)



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
from django.http import JsonResponse



import requests
from django.http import JsonResponse

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


# def filter_movies(request):
#     genre = request.GET.get("genre")
#     title_type = request.GET.get("titleType")
#     start_year = request.GET.get("startYear")
#     end_year = request.GET.get("endYear")

#     # Fetch movie data from the API
#     url = "https://moviesdatabase.p.rapidapi.com/titles"
#     headers = {
#         'X-RapidAPI-Key': 'ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b',
#         "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
#     }
    
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Raise an exception for non-2xx responses
#         movies_data = response.json()
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({"error": f"Failed to fetch movies from API: {str(e)}"}, status=500)

#     # Apply filtering to the fetched data
#     filtered_movies = []
#     for movie_data in movies_data.get("results", []):
#         if (
#             (not genre or genre in movie_data.get("genres", []))
#             and (not title_type or title_type == movie_data.get("titleType", ""))
#             and (not start_year or int(start_year) <= int(movie_data.get("releaseYear", 0)))
#             and (not end_year or int(end_year) >= int(movie_data.get("releaseYear", 0)))
#         ):
#             filtered_movies.append({"title": movie_data.get("titleText", "")})

#     return JsonResponse(filtered_movies, safe=False)



# def filter_movies(request):
#     genre = request.GET.get("genre")
#     title_type = request.GET.get("titleType")
#     start_year = request.GET.get("startYear")
#     end_year = request.GET.get("endYear")

#     # Fetch movie data from the API
#     url = "https://moviesdatabase.p.rapidapi.com/titles"
#     headers = {
#         'X-RapidAPI-Key': 'ede169c197msh94c9ec518d4a5e2p18d147jsn10e88d3b6b4b',
#         "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com",
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         return JsonResponse({"error": "Failed to fetch movies from API"}, status=500)
    
#     movies_data = response.json()

#     # Apply filtering to the fetched data
#     filtered_movies = []
#     for movie_data in movies_data["results"]:
#         if (
#             (not genre or genre in movie_data["genre"])
#             and (not title_type or title_type == movie_data["titleType"])
#             and (not start_year or int(start_year) <= int(movie_data["releaseYear"]))
#             and (not end_year or int(end_year) >= int(movie_data["releaseYear"]))
#         ):
#             filtered_movies.append({"title": movie_data["titleText"]})

#     return JsonResponse(filtered_movies, safe=False)

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





class MovieViewSet(viewsets.ModelViewSet):
    queryset = movie.objects.all()
    serializer_class = movieSerializer