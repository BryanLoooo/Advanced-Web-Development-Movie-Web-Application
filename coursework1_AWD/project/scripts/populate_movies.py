import os
import sys
import django
import csv

# Add your Django project's base directory to the Python path
sys.path.append('C:/AdvancedWebDevelopment Mid Term Project/midTermProj_AWD/project/')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# Import models from the movies app
from movies.models import Movie, Genre, Star, Director

# File paths for the cleaned CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
movies_file = os.path.join(script_dir, 'cleaned_Movies.csv')
genres_file = os.path.join(script_dir, 'cleaned_Genres.csv')
stars_file = os.path.join(script_dir, 'cleaned_Stars.csv')
directors_file = os.path.join(script_dir, 'cleaned_Directors.csv')

# Clear existing records from the database
Movie.objects.all().delete()
Genre.objects.all().delete()
Star.objects.all().delete()
Director.objects.all().delete()

# Populate the Movies table
with open(movies_file, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    movies = {}  # Dictionary to store movies by title
    for row in csv_reader:
        movie = Movie.objects.create(
            movie=row['movie'],
            runtime=row['runtime'],
            certificate=row.get('certificate', ''),  # Handle optional fields
            rating=float(row['rating']),
            description=row.get('description', ''),
            votes=int(row['votes'])
        )
        movies[row['movie']] = movie  # Store the movie instance for reference

# Populate the Genres table
with open(genres_file, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie_title = row.get('movie')
        genre_list = row['genre'].split(', ')  # Split genres if multiple
        if movie_title in movies:
            movie = movies[movie_title]
            for genre in genre_list:
                Genre.objects.create(movie=movie, genre=genre)
        else:
            print(f"Movie with title '{movie_title}' not found in Movies table. Skipping genre.")

# Populate the Stars table
with open(stars_file, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie_title = row.get('movie')
        star_name = row.get('stars')
        if movie_title in movies:
            movie = movies[movie_title]
            Star.objects.create(movie=movie, star_name=star_name)
        else:
            print(f"Movie with title '{movie_title}' not found in Movies table. Skipping star.")

# Populate the Directors table
with open(directors_file, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        movie_title = row.get('movie')
        director_name = row.get('director')
        if movie_title in movies:
            movie = movies[movie_title]
            Director.objects.create(movie=movie, director_name=director_name)
        else:
            print(f"Movie with title '{movie_title}' not found in Movies table. Skipping director.")

# Print completion message
print("Database population complete.")