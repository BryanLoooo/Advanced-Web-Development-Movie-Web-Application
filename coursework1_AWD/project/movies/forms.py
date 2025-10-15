# Import necessary modules and libraries
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Movie

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
# RegistrationForm: Form for user registration
class RegistrationForm(forms.ModelForm):
    # Password fields for secure input
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Role selection based on predefined choices in User model
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Role")

    # Optional date of birth field with a date picker widget
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date of Birth"
    )

    class Meta:
        # Associate the form with the User model
        model = User
        fields = ['username', 'email', 'age', 'phone_number', 'address', 'date_of_birth', 'gender', 'role', 'password']

    def clean(self):
        # Custom validation for the form
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Ensure password and confirm_password match
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match! Please try again.")

        return cleaned_data

# LoginForm: Form for user login
class LoginForm(forms.Form):
    # Username and password fields
    username = forms.CharField(max_length=255, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self):
        # Custom validation for login
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # Authenticate the user with provided credentials
        user = authenticate(username=username, password=password)
        print(f"Debug: Username={username}, Password={password}, Authenticated User={user}")  # Debugging

        # Raise validation errors for invalid login or inactive account
        if user is None:
            raise forms.ValidationError("Invalid username or password! Please try again.")

        if not user.is_active:
            raise forms.ValidationError("This account is inactive. Please contact support.")

        cleaned_data['user'] = user
        return cleaned_data

# MovieForm: Form for movie-related operations
class MovieForm(forms.ModelForm):
    class Meta:
        # Associate the form with the Movie model
        model = Movie
        fields = ['movie', 'runtime', 'certificate', 'rating', 'description', 'votes']