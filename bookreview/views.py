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


@login_required
def edit_ticket(request, tickets_pk):
    ticket = Ticket.objects.get(pk=tickets_pk, user=request.user)
    if ticket.image:
        image_file = ticket.image.url
    else:
        image_file = ""
    
    if request.method == 'POST':
        form = forms.CreateTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()
            return redirect('home')
    else :
        data = {
            "title": ticket.title,
            "description": ticket.description,
            "image": image_file
        }
        form = forms.CreateTicketForm(initial=data)
    return render(request, 'bookreview/edit_ticket.html', context={'form': form, 'image_file': image_file})
    