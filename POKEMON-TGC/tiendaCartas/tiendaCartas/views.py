from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from ventacarta.models import Usuario, Carta, Venta
from decimal import Decimal
import locale

# Create your views here.


def home(request):
    return render(request, 'index.html')


# Sign Up

def signup(request):
    return render(request, 'signup.html')


# Sign In


def signin(request):
    return render(request, 'signin.html')


def compra(request):
    listaCartas = Carta.objects.all()
    ctx = {'listado': listaCartas}
    return render(request, 'compra.html', ctx)

 # CARRIT0



def carrito(request):
    if request.method == 'POST':
        producto = request.POST.get('producto')
        valor = Decimal(request.POST.get('valor'))

        venta = Venta(idCarta=producto, preciototal=valor)
        venta.save()

        return redirect('listar')
    else:
        objetos_agregados = Venta.objects.all()

        # Obtener el nombre de cada carta y agregarlo al objeto agregado
        for objeto in objetos_agregados:
            carta = Carta.objects.get(id=objeto.idCarta)
            objeto.nombreCarta = carta.nombre

        total = sum(float(objeto.preciototal) for objeto in objetos_agregados)

        ctx = {
            'objetos_agregados': objetos_agregados,
            'total': total
        }
        return render(request, 'carrito.html', ctx)


# GPT

# Agregar objeto al carrito
def agregarCarro(request):
    if request.method == 'POST':
        producto = request.POST.get('producto')
        valor = request.POST.get('valor')

        venta = Venta(idCarta=producto, preciototal=valor)
        venta.save()

        return redirect('listar')
    else:
        return HttpResponseNotAllowed(['POST'])

# Mostrar objetos agregados


def mostrarObjetosAgregados(request):
    objetos_agregados = Venta.objects.all()

    context = {
        'objetos_agregados': objetos_agregados
    }

    return render(request, 'carrito.html', context)


# QUITAR OBJETOS DEL CARRITO.


def eliminarCarta(request):
    if request.method == 'POST':
        producto = request.POST.get('producto')
        
        # Verificar si la carta existe en la compra y eliminarla
        try:
            venta = Venta.objects.get(idCarta=producto)
            venta.delete()
            return HttpResponse("Carta eliminada correctamente")
        except Venta.DoesNotExist:
            return HttpResponse("La carta no existe en la compra")
    else:
        return HttpResponseNotAllowed(['POST'])




# INSERTAR REGISTROS:
def create(request, nuevoUsuario):
    usuarioNuevo = Usuario(nombre=nuevoUsuario)
    usuarioNuevo.save()
    return redirect(compra)


def delete(request, nuevoUsuario):
    personajeBorrar = Usuario.objects.filter(id__icontains=nuevoUsuario)
    personajeBorrar.delete()
    return redirect(compra)


def update(request, idUsuario, nuevoNombre):
    personajeActualizar = Usuario.objects.filter(id__icontains=idUsuario)
    personajeActualizar.update(nombre=nuevoNombre)
    return redirect(compra)
