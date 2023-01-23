from django import forms
from . import models

class TicketForm(forms.ModelForm):
    title = forms.CharField(label='Titre')

    class Meta: 
        model = models.Ticket
        fields = ['title', 'description', 'image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class ReviewForm(forms.ModelForm):
    headline = forms.CharField(label='Titre')

    CHOICES = [
        ('0', '- 0'),
        ('1', '- 1'),
        ('2', '- 2'),
        ('3', '- 3'),
        ('4', '- 4'),
        ('5', '- 5'),
    ]
    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=CHOICES)
    body = forms.CharField(label='Commentaire')
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)