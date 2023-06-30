from django.forms import ModelForm

from .models import Ticket, Review


class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


