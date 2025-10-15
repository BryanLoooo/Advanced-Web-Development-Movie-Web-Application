# Import necessary modules and libraries
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# UserManager: Manager class for user model
class UserManager(BaseUserManager):
    # Method for creating a standard user
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required.")
        if not email:
            raise ValueError("The Email field is required.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method for creating a superuser
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('age', 30)
        extra_fields.setdefault('phone_number', '')
        extra_fields.setdefault('address', '')
        extra_fields.setdefault('date_of_birth', None)
        extra_fields.setdefault('gender', 'prefer_not_to_say')

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get('role') != 'admin':
            raise ValueError("Superuser must have role='admin'.")

        return self.create_user(username, email, password, **extra_fields)

# User: Custom user model schema
class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('prefer_not_to_say', 'Prefer Not to Say'),
    ]

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    age = models.IntegerField(default=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True, default='')
    address = models.TextField(blank=True, null=True, default='')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='prefer_not_to_say')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.username} ({self.role})"

    def has_perm(self, perm, obj=None):
        return self.role == 'admin'

    def has_module_perms(self, app_label):
        return self.role == 'admin'

    @property
    def is_staff(self):
        return self.is_admin

# Movie: Movie table schema
class Movie(models.Model):
    movie = models.CharField(max_length=255, null=False, blank=False)
    runtime = models.CharField(max_length=50, null=False, blank=False)
    certificate = models.CharField(max_length=50, null=False, blank=False)
    rating = models.FloatField()
    description = models.TextField()
    votes = models.IntegerField()

    def __str__(self):
        return self.movie

# Genre: Genre table schema
class Genre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.genre

# Star: Star table schema
class Star(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    star_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.star_name

# Director: Director table schema
class Director(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.director_name