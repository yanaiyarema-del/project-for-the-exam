from django import forms
from .models import Book, Offer, Category

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'image', 'category']


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offered_book', 'requested_book']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['offered_book'].queryset = Book.objects.filter(owner=user)
            self.fields['requested_book'].queryset = Book.objects.exclude(owner=user)

