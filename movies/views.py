from django.shortcuts import render
# import requests
# from django.http import JsonResponse


# def random_movie(request):
#     api_key = 'd1b86ad384979557f58378a7c2b44912'
#     api_url = 'https://api.example.com/movies/random'  # Replace with the actual API URL

#     response = requests.get(api_url, params={'api_key': api_key})
#     if response.status_code == 200:
#         movie_data = response.json()
#         return JsonResponse(movie_data)
#     else:
#         return JsonResponse({'error': 'Unable to fetch movie data'}, status=500)
