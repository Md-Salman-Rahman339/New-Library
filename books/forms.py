from django import forms
from .models import Review, Book

class BookForm(forms.ModelForm):
    class Meta: 
        model = Book
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'user', 'comment']
