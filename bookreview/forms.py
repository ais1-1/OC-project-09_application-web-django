from django.forms import ModelForm, ChoiceField, RadioSelect

from .models import Ticket, Review


class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class CreateReviewForm(ModelForm):
    RATING_CHOICES = (
        ('0', 0),
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
    ) 
    rating = ChoiceField(required=True, choices=RATING_CHOICES, widget=RadioSelect)
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
