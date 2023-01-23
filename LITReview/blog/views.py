from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms, models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    tickets = sorted(tickets, key=lambda ticket: ticket.time_created, reverse=True)
    context = {
        'tickets': tickets
    }
    return render(request, 'blog/home.html', context=context)

@login_required
def posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    tickets = sorted(tickets, key=lambda ticket: ticket.time_created, reverse=True)
    context = {
        'tickets': tickets
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
    if request.method =='POST':
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

