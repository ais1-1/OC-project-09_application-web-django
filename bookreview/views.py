from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Ticket, Review, UserFollows

from . import forms


@login_required
def home(request):
    user = request.user
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    context = {"user" : user, "tickets": tickets, "reviews": reviews}
    return render(request, 'bookreview/home.html', context=context)


@login_required
def create_ticket(request):
    form = forms.CreateTicketForm()
    if request.method == 'POST':
        form = forms.CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render(request, 'bookreview/create_ticket.html', context={'form': form})
