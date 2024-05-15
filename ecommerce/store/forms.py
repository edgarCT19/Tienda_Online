from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'mark', 'price', 'quantity', 'oferta', 'description', 'qualityuno', 'qualitydos', 'qualitytres', 'qualitycuatro', 'qualitycinco', 'qualityseis', 'qualitysiete', 'qualityocho', 'qualitynueve', 'digital', 'section', 'image', 'imageuno', 'imagedos', 'imagetres', 'imagecuatro', 'imagecinco']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'mark': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'oferta': forms.Select(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25); --bs-dropdown-link-active-bg: var(--bs-danger)a', 'style':''}),
            'description': forms.Textarea(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'rows': 3}),
            'section': forms.Select(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'image': forms.FileInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'type':'file'}),
            'imageuno': forms.FileInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'type':'file'}),
            'imagedos': forms.FileInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'type':'file'}),
            'imagetres': forms.FileInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'type':'file'}),
            'imagecuatro': forms.FileInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'type':'file'}),
            'imagecinco': forms.FileInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)', 'type':'file'}),
            'qualityuno': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualitydos': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualitytres': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualitycuatro': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualitycinco': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualityseis': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualitysiete': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualityocho': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25)'}),
            'qualitynueve': forms.TextInput(attrs={'class': 'form-control focus-ring text-decoration-none border','style':'--bs-focus-ring-color: rgba(var(--bs-danger-rgb), .25'}),
        }


