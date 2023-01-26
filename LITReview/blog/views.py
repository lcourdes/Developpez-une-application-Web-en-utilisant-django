from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from . import forms, models
from itertools import chain


@login_required
def home(request):
    followed_users = User.objects.filter(followed_by__in=request.user.following.all())
    reviews = models.Review.objects.filter(Q(user__in=followed_users)|Q(user=request.user))
    tickets = models.Ticket.objects.filter(user__in=followed_users)
    my_tickets=models.Ticket.objects.filter(user=request.user)
    reviews_of_my_tickets= models.Review.objects.filter(ticket__in=my_tickets).exclude(user=request.user)
    tickets_and_reviews = sorted(
        chain(reviews, tickets, my_tickets, reviews_of_my_tickets), 
        key=lambda instance: instance.time_created, 
        reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'blog/home.html', context=context)

@login_required
def posts(request):
    reviews = models.Review.objects.filter(user=request.user)
    tickets = models.Ticket.objects.filter(user=request.user)
    tickets_and_reviews = sorted(
        chain(tickets, reviews), 
        key=lambda instance: instance.time_created, 
        reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'blog/posts.html', context=context)

@login_required
def ticket_create(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    return render (request, 'blog/ticket_create.html', context={'form':form})

def get_instance(request, model, id):
    try: 
        instance = model.objects.get(id=id)
    except ObjectDoesNotExist:
        raise PermissionDenied
    if request.user != instance.user:
        raise PermissionDenied
    return instance

@login_required
def ticket_edit(request, ticket_id):
    ticket = get_instance(request, models.Ticket, ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('posts')
    context = {
        'edit_form': edit_form,
        'ticket': ticket,
    }
    return render(request, 'blog/ticket_edit.html', context=context)

@login_required
def ticket_delete(request, ticket_id):
    ticket = get_instance(request, models.Ticket, ticket_id)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        delete_form = forms.DeleteTicketForm(request.POST)
        if delete_form.is_valid():
            ticket.delete()
            return redirect('posts')
    context = {
        'ticket': ticket,
        'delete_form': delete_form,
    }
    return render(request, 'blog/ticket_delete.html', context=context)

@login_required
def review_and_ticket_create(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.is_reviewed = True
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render (request, 'blog/review_and_ticket_create.html', context=context)

@login_required
def review_specific_ticket_create(request, ticket_id):
    ticket = get_instance(request, models.Ticket, ticket_id)
    review_form = forms.ReviewForm()
    if request.method =='POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid:
            ticket.is_reviewed = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket': ticket,
    }
    return render (request, 'blog/review_specific_ticket_create.html', context=context)


@login_required
def review_edit(request, review_id):
    review = get_instance(request, models.Review, review_id)
    edit_form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('posts')
    context = {
        'edit_form': edit_form,
        'review': review,
        'ticket': review.ticket,
    }
    return render(request, 'blog/review_edit.html', context=context)

@login_required
def review_delete(request, review_id):
    review = get_instance(request, models.Review, review_id)
    ticket = review.ticket
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        delete_form = forms.DeleteReviewForm(request.POST)
        if delete_form.is_valid():
            review.delete()
            ticket.is_reviewed = False
            ticket.save()
            return redirect('posts')
    context = {
        'review': review,
        'delete_form': delete_form,
        'ticket': ticket,
    }
    return render(request, 'blog/review_delete.html', context=context)

@login_required
def follow_users(request):
    follow_form = forms.UsersFollowForm()
    users = User.objects.all().exclude(id=request.user.id)
    context = {'users': users,}
    if request.method == 'POST' and "new-user-follow-button" in request.POST:
        follow_form = forms.UsersFollowForm(request.POST)
        if follow_form.is_valid():
            usersFollow = follow_form.save()
            usersFollow.save()
            return render(request, 'blog/follow_users.html', context=context)
    if request.method == 'POST' and "delete-user-follow-button" in request.POST:
        instance = models.UserFollows.objects.get(user=request.user, followed_user=request.POST['delete-user-follow-button'])
        instance.delete()
        return render(request, 'blog/follow_users.html', context=context)
    return render(request, 'blog/follow_users.html', context=context)