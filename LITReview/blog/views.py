from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models
from itertools import chain


@login_required
def home(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
    tickets_and_reviews = sorted(
        chain(tickets, reviews), 
        key=lambda instance: instance.time_created, 
        reverse=True)
    context = {
        'tickets_and_reviews': tickets_and_reviews
    }
    return render(request, 'blog/home.html', context=context)

@login_required
def posts(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
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

@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
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
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
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
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
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
    review = get_object_or_404(models.Review, id=review_id)
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
    review = get_object_or_404(models.Review, id=review_id)
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