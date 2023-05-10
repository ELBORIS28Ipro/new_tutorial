from django.shortcuts import render, redirect
# Create your views here.
from .models import *
from .form import OrderForm
from django.forms import inlineformset_factory
from.filters import OrderFilter


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
    orders = Orders.objects.filter(customer_id=pk_test)
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customers, 'orders': orders,  'order_count': order_count, 'myFilter': myFilter}
    return render(request, 'customer.html',  context)

def createOrder(request, pk):
    OrdersFormSet = inlineformset_factory(Customer, Orders, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrdersFormSet(queryset=Orders.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('printing POST:', request.POST)
        #form = OrderForm(request.POST)
        formset = OrdersFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset, }
    return render(request, 'order_form.html',  context)

def updateOrder(request, pk):
    order = Orders.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'order_form.html', context)

def deleteOrder(request, pk):
    order = Orders.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'delete.html', context)

