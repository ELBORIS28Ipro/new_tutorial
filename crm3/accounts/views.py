from django.shortcuts import render
# Create your views here.
from .models import *

def home(request):
    orders = Orders.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending':  pending}
    return render(request, 'dashboard.html', context)


def products(request):
    product = Product.objects.all()
    return render(request, 'products.html', {'products': product})


def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = Customer.order_set.all()

    context = {'customer': customers, 'orders': orders}
    return render(request, 'customer.html',  context)
