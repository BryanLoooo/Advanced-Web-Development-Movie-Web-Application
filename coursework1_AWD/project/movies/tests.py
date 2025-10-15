from django.test import TestCase, Client
from django.urls import reverse
from movies.models import Movie, Genre, Star, Director
from django.contrib.auth.models import User

class UserTests(TestCase):

    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username='adminTest',
            email='adminTest@example.com',
            password='Pass',
            is_staff=True
        )
        self.customer_user = User.objects.create_user(
            username='customerTest',
            email='customerTest@example.com',
            password='Pass'
        )
        self.client = Client()

    def test_admin_dashboard_access(self):
        self.client.login(username='adminTest', password='Pass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_customer_dashboard_access(self):
        self.client.login(username='customerTest', password='Pass')
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_access(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

class MovieTests(TestCase):

    def setUp(self):
        # Create sample movie and related entities
        self.movie = Movie.objects.create(
            movie="Test Movie",
            runtime="120",
            certificate="PG-13",
            rating=8.5,
            description="A test movie description.",
            votes=10000
        )
        self.genre = Genre.objects.create(movie=self.movie, genre="Action")
        self.star = Star.objects.create(movie=self.movie, star_name="Test Star")
        self.director = Director.objects.create(movie=self.movie, director_name="Test Director")
        self.client = Client()

    def test_movie_detail_view(self):
        response = self.client.get(reverse('movie_detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")
        self.assertContains(response, "Action")
        self.assertContains(response, "Test Star")
        self.assertContains(response, "Test Director")

    def test_movie_list_view(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Movie")

    def test_create_movie_view(self):
        self.client.login(username='adminTest', password='Pass')
        response = self.client.post(reverse('create_movie'), {
            'movie': "New Movie",
            'runtime': "150",
            'certificate': "R",
            'rating': 7.0,
            'description': "A new test movie description.",
            'votes': 5000
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(movie="New Movie").exists())

    def test_update_movie_view(self):
        self.client.login(username='adminTest', password='Pass')
        response = self.client.post(reverse('update_movie', args=[self.movie.id]), {
            'movie': "Updated Movie",
            'runtime': "140",
            'certificate': "PG",
            'rating': 9.0,
            'description': "An updated test movie description.",
            'votes': 15000
        })
        self.assertEqual(response.status_code, 302)
        updated_movie = Movie.objects.get(id=self.movie.id)
        self.assertEqual(updated_movie.movie, "Updated Movie")

    def test_delete_movie_view(self):
        self.client.login(username='adminTest', password='Pass')
        response = self.client.post(reverse('delete_movie', args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Movie.objects.filter(id=self.movie.id).exists())

class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser123',
            email='testuser123@example.com',
            password='Pass'
        )
        self.client = Client()

    def test_registration_view(self):
        response = self.client.post(reverse('register'), {
            'username': "newuser111",
            'email': "newuser111@example.com",
            'password': "Pass",
            'confirm_password': "Pass"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser111").exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': "testuser123",
            'password': "Pass"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('customer_dashboard'))

    def test_logout_view(self):
        self.client.login(username='testuser123', password='Pass')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
