from django.core.checks import messages
from django.db.models import query
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from accounts.models import Customer, Order, Product
from .form import CreateUserForm, CustomerForm, OrderForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .filter import OrderFilter
# Create your views here.
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.decorators import login_required



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers,
     'total_customer':total_customer, 'total_orders':total_orders,
     'delivered':delivered, 'pending':pending}

    return render(request, 'dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products':products})

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count =  orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request, 'customer.html', context)

def account(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        Username = request.POST.get('username')
        Password = request.POST.get('password')

        User = authenticate(request, username=Username, password=Password)
        if User is not None:
            login(request, User)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
        
    context = {}
    return render(request, 'login.html', context)

def LogoutUser(request):
	logout(request)
	return redirect('login')

@unauthenticated_user
def registerPage(request):
    form  = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for'+username)
            return redirect('login')
    contex = {'form':form}
    return render(request, 'register.html', contex)

def reset_password(request):
    pass

def update(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'order_form.html', context)

def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER', order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'order_form.html', context)

def delete_Order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'delete.html', context)

def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=2)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if formset.is_valid():
        formset.save()
        return redirect('/')
    context = {'form':formset}
    return render(request, 'order_form.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page():
    pass