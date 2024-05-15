from django.shortcuts import render
from .models import Chambre, Reservation
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import ReservationForm

def index(request):
    # Récupérer toutes les chambres depuis la base de données
    chambres = Chambre.objects.all()

    # Passer les chambres au template pour l'affichage
    return render(request, 'index.html', {'chambres': chambres})


def chambres(request):
    chambres = Chambre.objects.all()
    return render(request, 'chambres.html', {'chambres': chambres})

def show_chambre(request, chambre_id):
    chambre = Chambre.objects.get(id = chambre_id)
    return render(request, 'show_chambre.html', {'chambre' : chambre})

from django.db.models import Q
 
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
                chambre=chambre  # Associer la réservation à la chambre correspondante
            )
            return redirect('index')  # Redirigez vers une vue de confirmation
    else:
        form = ReservationForm()
    
    return render(request, 'create_reservation.html', {'form': form})

def add_reservation(request):
    title = request.GET.get("title")
    start = request.GET.get("start")
    end = request.GET.get("end")
    reservation = Reservation(name=title, start=start, end=end)
    reservation.save()
    data = {}
 
    return JsonResponse(data)
