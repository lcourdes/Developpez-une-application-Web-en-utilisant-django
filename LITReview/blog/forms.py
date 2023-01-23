from django import forms
from . import models

class TicketForm(forms.ModelForm):
    title = forms.CharField(label='Titre')

    class Meta: 
        model = models.Ticket
        fields = ['title', 'description', 'image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)