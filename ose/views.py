import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.backends import UserModel
from django.contrib.auth.forms import UsernameField
from django.forms.widgets import PasswordInput
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse,  HttpResponseRedirect
from .forms import MyRegForm, LoginForm, ChangeProfileForm, ChangePasswordForm
import datetime
from .models import *

# Create your views here

# User Registration
def userReg(request):
    if request.method=="POST":
        frm=MyRegForm(request.POST, request.FILES)
        try:
            frm.is_valid()
            frm.save()

            messages.success(request, 'Registration successfull')
            frm = MyRegForm()
        except Exception as e:
            messages.error(request, e)
    else:
        frm=MyRegForm()
    return render(request, 'ose/userReg.html',{'frm':frm})

#user Login
def userLogin(request):
    if request.method=="POST":
        frm=LoginForm(request=request,data=request.POST)
        try:
            frm.is_valid()
            uname=frm.cleaned_data['username']
            upass=frm.cleaned_data['password']
    
            user=authenticate(username=uname, password=upass) 
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        except Exception as e:
            messages.success(request, e)
    else:
        frm=LoginForm()
    return render(request, 'ose/userLog.html', {'frm':frm})

def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created= Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:	
		items = []
		order = {'get_cart_total': 0,'get_cart_items':0, 'shipping': False}
		cartItems = order['get_cart_items']

	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'ose/store.html', context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete= False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:	
		items = []
		order = {'get_cart_total': 0,'get_cart_items':0, 'shipping': False}
		cartItems = order['get_cart_items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'ose/cart.html', context)

def checkout(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created= Order.objects.get_or_create(customer= customer, complete= False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:	
		items = []
		order = {'get_cart_total': 0,'get_cart_items':0, 'shipping': False}
		cartItems = order['get_cart_items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render( request, 'ose/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created= Order.objects.get_or_create(customer= customer, complete= False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity +1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity -1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()	

	return JsonResponse('Item was added', safe=False)	

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_order:
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
                   
    else:
        print('User is not logged in..')    
    return JsonResponse('Payment Complete!', safe=False)

def contactus(request):
	return render(request,'ose/contactus.html')	

def about(request):
	return render(request,'ose/about.html')	

#Change Password after login
def userChngPass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            frm=ChangePasswordForm(user=request.user, data=request.POST)
            if frm.is_valid():
                frm.save()
                update_session_auth_hash(request, frm.user)
                messages.success(request, 'Your password has been change successfully')
        else:
            frm=ChangePasswordForm(user=request.user)
        return render(request, 'ose/userChngPass.html', {'frm':frm, 'fname':request.user.first_name})

#logout
def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/userlog')

#Change Profile after login
def userChngProfile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            frm=ChangeProfileForm(request.POST, instance=request.user)
            if frm.is_valid():
                frm.save()
                messages.success(request, 'Your profile has been changes successfully')
        else:
            frm=ChangeProfileForm(instance=request.user)
        return render(request, 'ose/userChngProfile.html', {'frm':frm, 'fname':request.user.first_name})
    else:
        return HttpResponseRedirect('/userlog')

