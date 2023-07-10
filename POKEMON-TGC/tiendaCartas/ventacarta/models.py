from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.




class Usuario (models.Model):
    idventa = models.CharField(max_length = 200, null= True)
    nombreu = models.CharField(max_length = 200,null= True)
    fNac = models.IntegerField(validators=[MinValueValidator(1920), MaxValueValidator(9999)],null= True)
    email = models.EmailField(max_length=254,null= True)
    contrasenia = models.CharField(max_length=200, null= True)
    direccion = models.CharField(max_length = 200,null= True)




class Carta (models.Model):
    nombre = models.CharField(max_length = 200, null= True)
    anio = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], null= True)
    precio = models.DecimalField(max_digits=12,decimal_places=2, null= True)
    imagen = models.CharField(max_length = 1000, null= True)


class Venta (models.Model):
    idCarta = models.PositiveIntegerField(null= True)
    preciototal = models.DecimalField(max_digits=12,decimal_places=2, null= True)
    


