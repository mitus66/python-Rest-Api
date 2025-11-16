# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup(request):
    """Представлення для реєстрації користувачів"""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматично входимо користувача після реєстрації
            return redirect('quotes:index')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})