from django.db import models

class Chambre(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    taille = models.CharField(max_length=20)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='chambres/', blank=True)

    class Meta:
        db_table = "chambres"

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True) 
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='reservations', null=True, blank=True)

    class Meta:
        db_table = "reservations"