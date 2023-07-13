from django import forms

from .models import Ticket, Review, UserFollows


class UserSubscriptionForm(forms.ModelForm):
    followed_user = forms.CharField(
        label=("Suivre d'autres utilisateurs"),
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
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


class DeleteForm(forms.Form):
    delete_form = forms.BooleanField(widget=forms.HiddenInput, initial=True)
