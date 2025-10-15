from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from rest_framework import viewsets, generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Movie, Genre, Star, Director
from .serializers import (
    UserSerializer, MovieSerializer, GenreSerializer,
    StarSerializer, DirectorSerializer, LoginSerializer,
    CreateMovieSerializer, UserRegistrationSerializer
)
from .forms import LoginForm, MovieForm, RegistrationForm
import requests


# Login View
class LoginView(APIView):
    """
    Handles user login using Django REST Framework and renders the login.html page.
    """
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        if request.content_type == "application/json":
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
            else:
                return Response({"detail": "Invalid form submission.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
            else:
                return render(request, 'login.html', {'form': form, 'error': "Invalid form submission."})

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin-dashboard')
            return redirect('customer-home')
        return render(request, 'login.html', {'form': form, 'error': "Invalid username or password."})


# Customer Home View
class CustomerHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_home.html'


# Admin Dashboard View
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'


# Top Movies View
class TopMoviesView(View):
    def get(self, request):
        api_url = "http://127.0.0.1:8000/api/movies/top/"
        try:
            response = requests.get(api_url)
            top_rated_movies = response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching top-rated movies: {e}")
            top_rated_movies = []
        return render(request, "customer-top-movies.html", {"top_rated_movies": top_rated_movies})


# Movie Detail View
class MovieDetailView(View):
    def get(self, request, pk):
        api_url = f"http://127.0.0.1:8000/api/movies/{pk}/"
        try:
            response = requests.get(api_url)
            movie = response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie details: {e}")
            movie = None
        return render(request, "customer-movie-detail.html", {"movie": movie})


# Registration View
class RegistrationView(APIView):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        if request.content_type == "application/json":
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"detail": "Registration successful!"}, status=status.HTTP_201_CREATED)
            return Response({"detail": "Invalid registration data.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('customer-home')
            return render(request, 'register.html', {'form': form, 'error': "Invalid form submission."})


# Create Movie View
class CreateMovieView(LoginRequiredMixin, View):
    def get(self, request):
        form = MovieForm()
        return render(request, 'admin-create-movie.html', {'form': form})

    def post(self, request):
        form = MovieForm(request.POST)
        if form.is_valid():
            serializer = CreateMovieSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                serializer.save()
                return redirect('admin-dashboard')
            return render(request, 'admin-create-movie.html', {'form': form, 'error': serializer.errors})
        return render(request, 'admin-create-movie.html', {'form': form, 'error': 'Invalid form submission'})


# Read Movies View
class ReadMoviesView(View):
    def get(self, request):
        api_url = "http://127.0.0.1:8000/api/movies/"
        try:
            response = requests.get(api_url)
            movies = response.json() if response.status_code == 200 else []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movies: {e}")
            movies = []
        return render(request, "admin-read-movies.html", {"movies": movies})


# Update Movie View
class UpdateMovieView(View):
    def get(self, request, movie_id):
        api_url = f"http://127.0.0.1:8000/api/movies/{movie_id}/"
        try:
            response = requests.get(api_url)
            movie_data = response.json() if response.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie data: {e}")
            return redirect('read_movies')
        form = MovieForm(initial=movie_data)
        return render(request, "update-movie.html", {"form": form, "movie_id": movie_id})

    def post(self, request, movie_id):
        api_url = f"http://127.0.0.1:8000/api/movies/{movie_id}/"
        form = MovieForm(request.POST)
        if form.is_valid():
            try:
                response = requests.put(api_url, json=form.cleaned_data)
                if response.status_code == 200:
                    return redirect('read_movies')
            except requests.exceptions.RequestException as e:
                print(f"Error updating movie: {e}")
        return render(request, "update-movie.html", {"form": form, "movie_id": movie_id, "error": "Failed to update movie"})


# Delete Movie View
class DeleteMovieView(LoginRequiredMixin, View):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        return render(request, 'admin-delete-movie.html', {'movie': movie})

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        movie.delete()
        return redirect('read_movies')
