from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import get_object_or_404, redirect, render
from . import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib import messages

# Create your views here.

def home(request):
	return render(request, 'goutex/home.html')


def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'goutex/produtos.html', context)

def search(request):
    searchValue = request.GET.get('q','').strip()
    if searchValue == '':
        return redirect('store')
    products = Product.objects.filter(
		Q(name__icontains=searchValue)|
		Q(description__icontains=searchValue)|
		Q(category__name__icontains=searchValue)
		)
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {
		'cardItems':cartItems,
        'products': products,
        'searchValue' : searchValue
    }
    return render(request, 'goutex/produtos.html', context)


def singleProduto(request, productId):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	singleproduto = get_object_or_404(models.Product, id=productId)

	products = Product.objects.all()
	context = {'product':singleproduto, 'cartItems':cartItems}
	# id = { 'product': singleProduto }
	return render(request, 'goutex/singleProduto.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'goutex/carrinho.html', context)

def rastreio(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'goutex/rastreio.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'goutex/checkout.html', context)

def updateItem(request):
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

	return JsonResponse('Item was added', safe=False)

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