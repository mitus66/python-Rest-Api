from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Author, Quote
from .forms import AuthorForm, QuoteForm, CustomUserCreationForm

def index(request):
    quotes = Quote.objects.all().order_by('-created_at') # Сортуємо за датою створення
    return render(request, 'quotes_app/index.html', {'quotes': quotes})

def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes_app/author_detail.html', {'author': author})

def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("quotes_app:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = CustomUserCreationForm()
    return render(request, "quotes_app/register.html", {"register_form": form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("quotes_app:index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "quotes_app/login.html", {"login_form": form})

@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("quotes_app:index")

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Автор успішно доданий!")
            return redirect('quotes_app:index')
    else:
        form = AuthorForm()
    return render(request, 'quotes_app/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Цитата успішно додана!")
            return redirect('quotes_app:index')
    else:
        form = QuoteForm()
    return render(request, 'quotes_app/add_quote.html', {'form': form})

