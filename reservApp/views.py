from django.shortcuts import render
from .models import Chambre, Reservation
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import ReservationForm 
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

@login_required
def index(request):
    # Récupérer toutes les chambres depuis la base de données
    chambres = Chambre.objects.all()

    # Passer les chambres au template pour l'affichage
    return render(request, 'index.html', {'chambres': chambres})

@login_required
def chambres(request):
    chambres = Chambre.objects.all()
    return render(request, 'chambres.html', {'chambres': chambres})

@login_required
def show_chambre(request, chambre_id):
    chambre = Chambre.objects.get(id = chambre_id)
    return render(request, 'show_chambre.html', {'chambre' : chambre})

from django.db.models import Q

@login_required
def create_reservation(request, chambre_id):
    chambre = Chambre.objects.get(pk=chambre_id)  # Récupérer la chambre correspondant à l'ID
    context = {'chambre': chambre}

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            end_date = form.cleaned_data['end_date']
            end_time = form.cleaned_data['end_time']
           
            # Combiner la date et l'heure de début et de fin
            start = datetime.combine(start_date, start_time)
            end = datetime.combine(end_date, end_time)
           
            # Vérifier s'il existe déjà une réservation pour cette chambre sur ce créneau horaire
            if Reservation.objects.filter(chambre=chambre).filter(
                    Q(start__lt=end, end__gt=start) |
                    Q(start__lte=start, end__gte=end)
                ).exists():
                # Si une réservation existe déjà, renvoyer une erreur ou afficher un message à l'utilisateur
                return HttpResponse("Une réservation existe déjà pour cette chambre sur ce créneau horaire.")
           
            # Créer une nouvelle réservation associée à la chambre spécifiée
            nouvelle_reservation = Reservation.objects.create(
                name=name,
                start=start,
                end=end,
                chambre=chambre , # Associer la réservation à la chambre correspondante
                author=request.user,  # Associer la réservation à l'utilisateur connecté
            )
            return redirect('confirm_reservation', chambre_id=nouvelle_reservation.chambre.id)  # Redirigez vers une vue de confirmation
    else:
        form = ReservationForm()
    
    return render(request, 'create_reservation.html', {'form': form})

@login_required
def add_reservation(request):
    title = request.GET.get("title")
    start = request.GET.get("start")
    end = request.GET.get("end")
    reservation = Reservation(name=title, start=start, end=end, author=request.user)
    reservation.save()
    data = {}
 
    return JsonResponse(data)

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
            user.refresh_from_db()  # Charger le profil utilisateur créé automatiquement
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


