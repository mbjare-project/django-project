from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import os
import requests
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .utils import get_nifty_50_data, get_nifty_bank_data


def home(request):
    return render(request, 'home.html', {'title': 'Home'})

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def services(request):
    return render(request, 'services.html', {'title': 'Services'})

def market_overview(request):
    return render(request, 'market_overview.html')

def stock_screener(request):
    return render(request, 'stock_screener.html')

def portfolio_tracker(request):
    return render(request, 'portfolio_tracker.html')

def news(request):
    return render(request, 'news.html')


def login_view(request):
    # Handle login functionality
    if request.method == 'POST':
        username = request.POST.get('username')  # Using .get() for safety
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Display an error if authentication fails
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    # Handle logout functionality
    logout(request)
    return redirect('home')

# @login_required
# def profile_view(request):
#     # Only accessible when logged in
#     return render(request, 'profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile.html', context)

# def stock_view(request):
#     stock_symbol = 'AAPL'  # You can replace this with any stock symbol or make it dynamic via user input.
#     stock_data = get_stock_data(stock_symbol)
    
#     if stock_data:
#         context = {'stock_data': stock_data}
#     else:
#         context = {'error': 'Failed to retrieve stock data.'}
    
#     return render(request, 'stock.html', context)

def nifty_50_view(request):
    nifty_50_data = get_nifty_50_data()
    
    if nifty_50_data:
        context = {'nifty_50_data': nifty_50_data}
    else:
        context = {'error': 'Failed to retrieve Nifty 50 data.'}
    
    return render(request, 'nifty_50.html', context)




def nifty_bank_view(request):
    nifty_bank_data = get_nifty_bank_data()
    
    if nifty_bank_data:
        return render(request, 'nifty_bank.html', {'nifty_bank_data': nifty_bank_data})
    else:
        error = "Failed to retrieve Nifty Bank data."
        return render(request, 'nifty_bank.html', {'error': error})