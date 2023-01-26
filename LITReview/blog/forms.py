from django import forms
from . import models

class TicketForm(forms.ModelForm):
    class Meta: 
        model = models.Ticket
        fields = ['title', 'description', 'image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class UsersFollowForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['user', 'followed_user']
