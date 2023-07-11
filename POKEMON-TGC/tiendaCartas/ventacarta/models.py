from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(models.Model):
    nombreu = models.CharField(max_length=200, null=True)
    fNac = models.IntegerField(validators=[MinValueValidator(1920), MaxValueValidator(9999)], null=True)
    email = models.EmailField(max_length=254, null=True)
    contrasenia = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    sesion = models.BooleanField(default=False)  # Nuevo campo para verificar si el usuario está en sesión
    venta_asociada = models.ForeignKey('Venta', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='usuario_venta')  # Nueva relación con la venta


class Carta(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    anio = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)], null=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    imagen = models.CharField(max_length=1000, null=True)
    ventas_relacionadas = models.ManyToManyField('Venta')


class Venta(models.Model):
    id_carta = models.ForeignKey(Carta, on_delete=models.CASCADE, null=True, default=None)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, default=None)
    preciototal = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        # Actualizar el campo preciototal antes de guardar la venta
        self.preciototal = self.cartas_seleccionadas().aggregate(models.Sum('precio'))['precio__sum'] or 0
        super().save(*args, **kwargs)

    def cartas_seleccionadas(self):
        return self.id_carta.all()

    def asignar_venta_a_usuario(self, usuario):
        if usuario.sesion:
            self.id_usuario = usuario
            self.save()
