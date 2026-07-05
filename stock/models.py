from django.db import models

class Warehouse(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    capacite = models.IntegerField()

    def __str__(self):
        return f"{self.nom} ({self.localisation})"
    

class Product(models.Model):
   
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('reserve', 'Réservé'),
        ('perime', 'Périmé'),
    ]

    nom = models.CharField(max_length=100)
    quantite = models.IntegerField()
    date_expiration = models.DateField()
    etat = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return f"{self.nom} - Qté: {self.quantite} ({self.etat})"    