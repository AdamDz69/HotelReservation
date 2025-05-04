# views.py

from django.shortcuts import render, redirect
from .models import Chambre, Reservation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import ReservationForm, SignUpForm
from django.contrib.auth import login, authenticate

@login_required
def index(request):
    chambres = Chambre.objects.all()
    return render(request, 'index.html', {'chambres': chambres})

@login_required
def chambres(request):
    chambres = Chambre.objects.all()
    return render(request, 'chambres.html', {'chambres': chambres})

@login_required
def show_chambre(request, chambre_id):
    chambre = Chambre.objects.get(id=chambre_id)
    return render(request, 'show_chambre.html', {'chambre': chambre})

from django.db.models import Q

@login_required
def create_reservation(request, chambre_id):
    chambre = Chambre.objects.get(pk=chambre_id)
    context = {'chambre': chambre}

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            end_date = form.cleaned_data['end_date']
            end_time = form.cleaned_data['end_time']
            start = datetime.combine(start_date, start_time)
            end = datetime.combine(end_date, end_time)
            
            if Reservation.objects.filter(chambre=chambre).filter(
                    Q(start__lt=end, end__gt=start) |
                    Q(start__lte=start, end__gte=end)
                ).exists():
                return HttpResponse("Une réservation existe déjà pour cette chambre sur ce créneau horaire.")
            
            nouvelle_reservation = Reservation.objects.create(
                name=name,
                start=start,
                end=end,
                chambre=chambre,
                author=request.user,
            )
            return redirect('confirm_reservation', chambre_id=nouvelle_reservation.chambre.id)
    else:
        form = ReservationForm()

    return render(request, 'create_reservation.html', {'form': form})

@login_required
def confirm_reservation(request, chambre_id):
    chambre = Chambre.objects.get(pk=chambre_id)
    reservation = Reservation.objects.filter(chambre=chambre).last()
    return render(request, 'confirm_reservation.html', {'reservation': reservation})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Vue pour afficher ggmap.html
def ggmap_view(request):
    return render(request, 'ggmap.html')
