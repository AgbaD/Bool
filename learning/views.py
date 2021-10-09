from .models import Movies
from rest_framework.response import Response
from rest_framework import status
from .serializers import MoviesSerializer
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['GET'])
def movies(request):
    if request.method == 'GET':
        all_movies = Movies.objects.all()
        serializer = MoviesSerializer(all_movies, many=True)
        return Response(serializer.data)
