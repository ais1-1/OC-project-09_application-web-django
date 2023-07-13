from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from itertools import chain
from django.contrib.auth import get_user_model


from .models import Ticket, Review, UserFollows
from . import forms


User = get_user_model()


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 4)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    tickets_pk_with_response = []
    for ticket in tickets:
        if ticket.review_set.count() == 1:
            tickets_pk_with_response.append(ticket.pk)

    context = {
        "page_obj": page_obj,
        "tickets_pk_with_response": tickets_pk_with_response,
    }
    return render(request, "bookreview/home.html", context=context)


@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    return render(request, "bookreview/my_posts.html", context=context)


@login_required
def create_ticket(request):
    form = forms.CreateTicketForm()
    if request.method == "POST":
        form = forms.CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    return render(request, "bookreview/create_ticket.html", context={"form": form})


@login_required
def edit_ticket(request, tickets_pk):
    ticket = get_object_or_404(Ticket, pk=tickets_pk, user=request.user)
    if ticket.image:
        image_file = ticket.image.url
    else:
        image_file = ""

    if request.method == "POST":
        form = forms.CreateTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.save()
            return redirect("home")
    else:
        data = {
            "title": ticket.title,
            "description": ticket.description,
            "user": ticket.user,
            "image": image_file,
            "time_created": ticket.time_created,
        }
        form = forms.CreateTicketForm(initial=data)
    return render(
        request,
        "bookreview/edit_ticket.html",
        context={"form": form, "image_file": image_file},
    )


@login_required
def delete_ticket(request, tickets_pk):
    ticket = get_object_or_404(Ticket, pk=tickets_pk, user=request.user)
    delete_form = forms.DeleteForm()
    if request.method == "POST":
        if "delete_form" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("home")
    return render(
        request,
        "bookreview/delete_ticket.html",
        context={"delete_form": delete_form, "ticket": ticket},
    )


@login_required
def create_review(request):
    ticket_form = forms.CreateTicketForm()
    review_form = CreateReviewForm()
    if request.method == "POST":
        ticket_form = forms.CreateTicketForm(request.POST, request.FILES)
        review_form = forms.CreateReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect("home")
    return render(
        request,
        "bookreview/create_review.html",
        context={"ticket_form": ticket_form, "review_form": review_form},
    )


@login_required
def edit_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    ticket = review.ticket
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST, instance=review)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.ticket = ticket
            form_instance.user = request.user
            form_instance.save()
            return redirect("home")
    else:
        data = {
            "ticket": ticket,
            "rating": review.rating,
            "headline": review.headline,
            "body": review.body,
            "user": review.user,
            "time_created": review.time_created,
        }
        form = forms.CreateReviewForm(initial=data)
    return render(
        request, "bookreview/edit_review.html", context={"form": form, "ticket": ticket}
    )


@login_required
def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    delete_form = forms.DeleteForm()
    if request.method == "POST":
        if "delete_form" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("home")
    return render(
        request,
        "bookreview/delete_review.html",
        context={"delete_form": delete_form, "review": review},
    )


@login_required
def create_review_as_response(request, tickets_pk):
    ticket = get_object_or_404(Ticket, pk=tickets_pk)
    form = forms.CreateReviewForm()
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.ticket = ticket
            form_instance.user = request.user
            form_instance.save()
            return redirect("home")
    return render(
        request,
        "bookreview/review_as_response.html",
        context={"form": form, "ticket": ticket},
    )


@login_required
def follow_users(request):
    followed_users = UserFollows.objects.filter(user=request.user)
    user_followees = UserFollows.objects.filter(followed_user=request.user)
    form = forms.UserSubscriptionForm(initial={"user": ""})
    if request.method == "POST":
        form = forms.UserSubscriptionForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.follow = form.cleaned_data["followed_user"]
            form_instance.save()
            return redirect("home")
    return render(
        request,
        "bookreview/subscriptions.html",
        context={
            "form": form,
            "followed_users": followed_users,
            "user_followees": user_followees,
        },
    )


@login_required
def unfollow_user(request, user_pk):
    followed_user = get_object_or_404(User, pk=user_pk)
    user_follows = get_object_or_404(
        UserFollows, user=request.user, followed_user=followed_user
    )
    delete_form = forms.DeleteForm()
    if request.method == "POST":
        if "delete_form" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                user_follows.delete()
                return redirect("home")
    return render(
        request,
        "bookreview/unfollow.html",
        context={"delete_form": delete_form, "user_follows": user_follows},
    )
