from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q

# Create your views here.
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import TradingHistory, CryptoBase, CryptoCoin, Profile
from .forms import CreateUserForm, TradingHistoryForm, TradingHistorySearchForm
# testing https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2

@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
@admin_only
def index(request):
    """
    Dashboard para administrar trading
    """
    orders = TradingHistory.objects.all()
    form = TradingHistorySearchForm(request.GET, user=request.user)
    
    if form.is_valid():
        if form.cleaned_data['status']:
            status = form.cleaned_data['status']
            lg = len(status)
            if lg == 1:
                orders = orders.filter(status__icontains=status[0])
            elif lg == 2:
                orders = orders.filter(Q(status__icontains=status[0]) | Q(status__icontains=status[1]))
        if form.cleaned_data['type_order']:
            type_order = form.cleaned_data['type_order']
            lg = len(type_order)
            if lg == 1:
                orders = orders.filter(type_order__icontains=type_order[0])
            elif lg == 2:
                orders = orders.filter(Q(type_order__icontains=type_order[0]) | Q(type_order__icontains=type_order[1]))
        if form.cleaned_data['start_date']:
            start_date = form.cleaned_data['start_date']
            orders = orders.filter(date__gte=start_date)
        if form.cleaned_data['end_date']:
            end_date = form.cleaned_data['end_date']
            orders = orders.filter(date__lt=end_date)
        if form.cleaned_data['coin_search']:
            coin_search = form.cleaned_data['coin_search']
            orders = orders.filter(coin__id=coin_search.id)
        if form.cleaned_data['base_search']:
            base_search = form.cleaned_data['base_search']
            orders = orders.filter(base__id=base_search.id)
        if form.cleaned_data['profile']:
            profile = form.cleaned_data['profile']
            orders = orders.filter(profile__id=profile.id)
        
        form = TradingHistorySearchForm(user=request.user)
    context = {"form": form, "orders": orders}
    return render(request, './index.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['users_group'])
def userPage(request):
    orders = request.user.profile.tradinghistory_set.all()
    form = TradingHistorySearchForm(request.GET, user=request.user)

    if form.is_valid():
        if form.cleaned_data['status']:
            status = form.cleaned_data['status']
            lg = len(status)
            if lg == 1:
                orders = orders.filter(status__icontains=status[0])
            elif lg == 2:
                orders = orders.filter(Q(status__icontains=status[0]) | Q(status__icontains=status[1]))
        
        if form.cleaned_data['type_order']:
            type_order = form.cleaned_data['type_order']
            lg = len(type_order)
            if lg == 1:
                orders = orders.filter(type_order__icontains=type_order[0])
            elif lg == 2:
                orders = orders.filter(Q(type_order__icontains=type_order[0]) | Q(type_order__icontains=type_order[1]))
        if form.cleaned_data['start_date']:
            start_date = form.cleaned_data['start_date']
            orders = orders.filter(date__gte=start_date)
        if form.cleaned_data['end_date']:
            end_date = form.cleaned_data['end_date']
            orders = orders.filter(date__lt=end_date)
        if form.cleaned_data['coin_search']:
            coin_search = form.cleaned_data['coin_search']
            orders = orders.filter(coin__id=coin_search.id)
        if form.cleaned_data['base_search']:
            base_search = form.cleaned_data['base_search']
            orders = orders.filter(base__id=base_search.id)
        form = TradingHistorySearchForm(user=request.user)

    context = {"form": form, "orders": orders}
    return render(request, 'accounts/user.html', context)


@unauthenticated_user
def registerPage(request):
    """
    Registrar nuevos usuarios
    """
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save() # signal se llama después de esto
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, './register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # login exitoso
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, './login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# CRUDL for trading history
# https://techpluslifestyle.com/technology/django-crud-operation-using-function-based-views/
@login_required(login_url='login')
def trading_history_create(request):
    context= {}
    form = TradingHistoryForm(request.POST or None)
    if form.is_valid():
        user = request.user
        profile = Profile.objects.get(user=user)
        order = form.save(commit=False)
        order.profile = profile
        order.status = "Open"
        order.save()
        return redirect('home')

    context["form"] = form
    return render(request, "./history_form.html", context)

@login_required(login_url='login')
def trading_history_update(request, pk):

    order = get_object_or_404(TradingHistory, pk=pk)
    form = TradingHistoryForm(request.POST or None, instance=order)
    if form.is_valid():
        buy = form.cleaned_data.get('buy_price')
        if buy is not None:
            order.buy_price = buy
            type_order = order.type_order
            if type_order == "Buy":
                order.total = (order.sell_price - order.buy_price) * order.amount
            elif type_order == "Sell":
                order.total = ( order.buy_price - order.sell_price) * order.amount
        
        form.save()
        return redirect('home')

    context = {"form": form}

    return render(request, "history_form.html", context)

@login_required(login_url='login')
def trading_history_delete(request, pk):
    order = get_object_or_404(TradingHistory, pk=pk)

    if request.method == "POST":
        order.delete()
        return redirect('home')
    context = {'order': order}
    return render(request, "./delete.html", context)


def trading_history_close(request, pk):
    order = get_object_or_404(TradingHistory, pk=pk)

    if request.method == "POST":
        close_price = request.POST.get('close_price')
        order.sell_price = float(close_price)

        type_order = order.type_order
        if type_order == "Buy":
            order.total = (order.sell_price - order.buy_price) * order.amount
        elif type_order == "Sell":
            order.total = ( order.buy_price - order.sell_price) * order.amount
        order.status = "Close"
        order.save()
        return redirect('home')
    context = {'order': order}
    return render(request, "accounts/close.html", context)