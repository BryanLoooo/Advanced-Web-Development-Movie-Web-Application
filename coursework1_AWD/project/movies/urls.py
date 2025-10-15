from django.urls import path
from .views import LoginView, CustomerHomeView
from .views import TopMoviesView
from .views import MovieDetailView
from .views import RegistrationView, AdminDashboardView
from .api import (
    UserList, UserDetails,
    MovieList, MovieDetails,
    GenreList, GenreDetails,
    StarList, StarDetails,
    DirectorList, DirectorDetails,
)

from .api import TopRatedMoviesAPIView
from .api import MovieDetail
from .api import UserRegister
from .views import CreateMovieView
from .api import CreateMovieAPIView
from .views import DeleteMovieView
from .api import DeleteMovieAPIView
from .views import ReadMoviesView
from .views import UpdateMovieView

urlpatterns = [
    path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetails.as_view(), name='user-details'),
    path('api/movies/', MovieList.as_view(), name='movie-list'),
    path('api/movies/<int:pk>/', MovieDetails.as_view(), name='movie-details'),
    path('api/genres/', GenreList.as_view(), name='genre-list'),
    path('api/genres/<int:pk>/', GenreDetails.as_view(), name='genre-details'),
    path('api/stars/', StarList.as_view(), name='star-list'),
    path('api/stars/<int:pk>/', StarDetails.as_view(), name='star-details'),
    path('api/directors/', DirectorList.as_view(), name='director-list'),
    path('api/directors/<int:pk>/', DirectorDetails.as_view(), name='director-details'),
    
    path("api/movies/top/", TopRatedMoviesAPIView.as_view(), name="top-rated-movies-api"),
    path('api/movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('api/register/', UserRegister.as_view(), name='register-api'),

    path('api/login/', LoginView.as_view(), name='login'),
    path('customer-home/', CustomerHomeView.as_view(), name='customer-home'),
    path("top-movies/", TopMoviesView.as_view(), name="top-movies"),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('create-movie/', CreateMovieView.as_view(), name='create_movie'),  # HTML form view
    path('api/movies/create/', CreateMovieAPIView.as_view(), name='create_movie_api'),  # API endpoint
    path('delete-movie/<int:movie_id>/', DeleteMovieView.as_view(), name='delete_movie'),  # HTML form view
    path('api/movies/delete/<int:id>/', DeleteMovieAPIView.as_view(), name='delete_movie_api'),  # API endpoint
     path('update-movie/<int:movie_id>/', UpdateMovieView.as_view(), name='update_movie'),  
    path('read-movies/', ReadMoviesView.as_view(), name='read_movies'),
]
