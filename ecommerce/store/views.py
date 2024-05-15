from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import SignupForm, LoginForm
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import urllib.request

# Create your views here.
# Home page
def index(request):
    return render(request, 'store/store.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario creado
            # Crea un objeto Customer asociado al usuario
            customer = Customer.objects.create(user=user)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  
                # Accede al objeto Customer asociado al usuario
                customer = user.customer
                # Luego redirecciona según sea necesario
                return redirect('store')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

# logout page
def user_logout(request):
    auth_logout(request)
    messages.info(request, 'Session Deleted')
    return redirect('store')

@login_required
def profile(request):
    data = cartData(request)
    user = request.user
    cartItems = data['cartItems']
    # Accede al objeto Customer asociado al usuario
    customer = user.customer
    return render(request, 'store/perfil.html', {'user': user, 'customer': customer, 'cartItems':cartItems})

@login_required
def order_history(request):
    data = cartData(request)
    cartItems = data['cartItems']
    user = request.user
    order_history = OrderHistory.objects.filter(user=user)
    return render(request, 'store/order_history.html', {'order_history': order_history, 'cartItems':cartItems})

@login_required
def add_product(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Asigna al usuario actual como el vendedor
            product.save()
            return redirect('profile')  # Redirige al perfil del usuario después de agregar el producto
    else:
        form = ProductForm(initial={'seller': request.user})  # Inicializa el formulario con el usuario actual
    return render(request, 'store/addProduct.html', {'form': form,'cartItems':cartItems})

@login_required
def product_history(request):
    data = cartData(request)
    cartItems = data['cartItems']
    user = request.user
    print("Usuario autenticado:", user.username)  # Verifica el usuario autenticado en la consola del servidor
    products = Product.objects.filter(seller=request.user)
    return render(request, 'store/productHistory.html', {'products': products, 'cartItems':cartItems})

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def main(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/main.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)


@login_required  # Asegura que el usuario esté autenticado
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    if request.method == 'POST':
        # Aquí se procesaría el pago...
        # Se crea un registro en OrderHistory
        if request.user.is_authenticated:
            OrderHistory.objects.create(user=request.user, order=order)
            messages.success(request, '¡Pago realizado con éxito! Tu pedido ha sido registrado.')
            # Simulación de seguimiento de pedido: se marca el pedido como completado y se actualiza el estado del pedido
            order.complete = True
            order.status = "En espera de envío"
            order.save()
            # Redirige al historial de pedidos
            return redirect('order_history')
        else:
            messages.error(request, '¡Debe iniciar sesión para realizar un pedido!')
            return redirect('login')  # Redirige al usuario a iniciar sesión si no lo está
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        # Devuelve una respuesta JSON indicando que la actualización se realizó correctamente
        return JsonResponse({'message': 'Item was updated', 'quantity': orderItem.quantity}, status=200)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=400)
    except KeyError as e:
        return JsonResponse({'error': 'Missing key in request data: ' + str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    # Restar la cantidad de productos comprados del stock
    for item in order.orderitem_set.all():
        product = item.product
        product.quantity -= item.quantity
        product.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)

