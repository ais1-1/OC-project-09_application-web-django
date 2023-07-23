from django import forms
from django.contrib.auth import get_user_model


from .models import Ticket, Review, UserFollows

User = get_user_model()


class UserSubscriptionForm(forms.ModelForm):
    followed_user = forms.CharField(
        label=(""),
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Nom d'utilisateur", "class": "form_control"}
        ),
    )

    class Meta:
        model = UserFollows
        fields = ["followed_user"]

    def clean_followed_user(self):
        followed_user_string = self.cleaned_data["followed_user"]

        try:
            followed_user = User.objects.get(username=followed_user_string)
        except User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")

        return followed_user


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form_control"}),
            "description": forms.Textarea(
                attrs={"class": "form_control text_form_control"}
            ),
            "image": forms.FileInput(attrs={"class": "form_control"}),
        }


class CreateReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        ("0", 0),
        ("1", 1),
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
    )
    rating = forms.ChoiceField(
        required=True, choices=RATING_CHOICES, widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "headline": forms.TextInput(attrs={"class": "form_control"}),
            "body": forms.Textarea(attrs={"class": "form_control text_form_control"}),
            "rating": forms.FileInput(attrs={"class": "form_control"}),
        }


class DeleteForm(forms.Form):
    delete_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
