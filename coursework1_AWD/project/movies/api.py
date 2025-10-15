from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import User, Movie, Genre, Star, Director
from .serializers import (
    UserSerializer, MovieSerializer, GenreSerializer,
    StarSerializer, DirectorSerializer
)

from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import DestroyAPIView
from .serializers import CreateMovieSerializer
from rest_framework.permissions import IsAuthenticated


# User API Views
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Movie API Views
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Genre API Views
class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

# Star API Views
class StarList(generics.ListCreateAPIView):
    queryset = Star.objects.all()
    serializer_class = StarSerializer

class StarDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Star.objects.all()
    serializer_class = StarSerializer

# Director API Views
class DirectorList(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class DirectorDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class TopRatedMoviesAPIView(APIView):
    """
    API view for fetching the top 10 rated movies.
    """

    def get(self, request, *args, **kwargs):
        # Fetch top 10 rated movies
        top_rated_movies = Movie.objects.order_by('-rating')[:10]
        serializer = MovieSerializer(top_rated_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MovieDetail(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateMovieAPIView(CreateAPIView):
    """
    API view to handle movie creation.
    """
    queryset = Movie.objects.all()
    serializer_class = CreateMovieSerializer
    permission_classes = [IsAuthenticated]

class DeleteMovieAPIView(DestroyAPIView):
    """
    API view to delete a movie by its ID.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'