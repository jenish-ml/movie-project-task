from django import forms
from .models import Movie
from category.models import Category

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'poster', 'description', 'release_date', 'actors', 'category', 'trailer_link']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'})
        }
