from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed
from ventacarta.models import Usuario, Carta, Venta
from decimal import Decimal

# Create your views here.


def home(request):
    return render(request, 'index.html')


# Sign Up

def signup(request):
    return render(request, 'signup.html')


# Sign In


def signin(request):
    return render(request, 'signin.html')




# LISTAR COPMRA

def compra(request):
    listaCartas = Carta.objects.all()
    ctx = {'listado': listaCartas}
    return render(request, 'compra.html', ctx)


def carrito(request):
    if request.method == 'POST':
        # Agregar producto al carrito
        producto = request.POST.get('producto')
        valor = Decimal(request.POST.get('valor'))

        carrito = request.session.get('carrito', [])
        carrito.append({'producto': producto, 'valor': valor})
        request.session['carrito'] = carrito

        return redirect('listar')
    else:
        carrito = request.session.get('carrito', [])
        objetos_agregados = []
        total = 0

        for item in carrito:
            carta = Carta.objects.get(id=item['producto'])
            nombre_carta = carta.nombre
            valor = item['valor']
            total += valor

            cartas_relacionadas = Venta.objects.filter(
                id_carta=item['producto'])

            objetos_agregados.append({
                'idCarta': item['producto'],
                'nombre': nombre_carta,
                'preciototal': valor,
                'cartas_relacionadas': cartas_relacionadas
            })

        ctx = {
            'objetos_agregados': objetos_agregados,
            'total': total
        }
        return render(request, 'carrito.html', ctx)


def agregarCarro(request):
    if request.method == 'POST':
        producto = request.POST.get('producto')
        valor = request.POST.get('valor')

        venta = Venta(id_carta_id=producto, preciototal=valor)
        venta.save()

        return redirect('listar')
    else:
        return HttpResponseNotAllowed(['POST'])


def mostrarObjetosAgregados(request):
    objetos_agregados = Venta.objects.all()

    context = {
        'objetos_agregados': objetos_agregados
    }

    return render(request, 'carrito.html', context)


def eliminarCarta(request):
    if request.method == 'POST':
        producto = request.POST.get('producto')
        carrito = request.session.get('carrito', [])
        for item in carrito:
            if item['producto'] == producto:
                carrito.remove(item)
                request.session['carrito'] = carrito
                break  
        return HttpResponse("Carta eliminada correctamente")
    else:
        return HttpResponseNotAllowed(['POST'])


# CARRITO DE COMPRAS:

@transaction.atomic
def listadoCarrito(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', [])
        total = request.POST.get('total')
        objetos_agregados = []
        for item in carrito:
            carta = Carta.objects.get(id=item['producto'])
            nombre_carta = carta.nombre
            valor = item['valor']
            cartas_relacionadas = Venta.objects.filter(id_carta=item['producto'])
            objetos_agregados.append({
                'idCarta': item['producto'],
                'nombre': nombre_carta,
                'preciototal': valor,
                'cartas_relacionadas': cartas_relacionadas
            })
            venta = Venta(id_carta=carta, preciototal=total)
            venta.save()
        del request.session['carrito']
        ctx = {
            'objetos_agregados': objetos_agregados,
            'total': total
        }
        return render(request, 'carrito.html', ctx)
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


def registro(request):
    if request.method == 'POST':
        nombreu = request.POST['nombreu']
        fNac = request.POST['fNac']
        email = request.POST['email']
        contrasenia = request.POST['contrasenia']
        direccion = request.POST['direccion']
        
        usuario = Usuario(nombreu=nombreu, email=email, direccion=direccion, contrasenia=contrasenia,)
        usuario.save()
        return redirect('signin') 