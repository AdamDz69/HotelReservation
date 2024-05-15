from django.urls import path
from . import views
from .views import index, chambres, show_chambre
from django.contrib import admin

urlpatterns = [
    path("",views.index,name="index"),
    path("chambres",views.chambres,name="chambres"),
    path("chambre/<int:chambre_id>/",views.show_chambre,name="show_chambre"),
    path('create_reservation/<int:chambre_id>', views.create_reservation, name='create_reservation'),

]
