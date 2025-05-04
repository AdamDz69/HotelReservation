from django.contrib import admin
from .models import Reservation
from .models import Chambre

class ReservationAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        # Vérifiez si l'utilisateur est un superutilisateur ou s'il a la permission 'can_view_all_reservations'
        if request.user.is_superuser or request.user.has_perm('reservApp.can_view_all_reservations'):
            return True
        return False

admin.site.register(Reservation, ReservationAdmin)

class ChambreAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        # Vérifiez si l'utilisateur est un superutilisateur ou s'il a la permission 'can_view_all_chambres'
        if request.user.is_superuser or request.user.has_perm('reservApp.can_view_all_chambres'):
            return True
        return False

admin.site.register(Chambre, ChambreAdmin)