# quotes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quote, Author
from .forms import AuthorForm, QuoteForm


def index(request):
    # Тепер цей рядок працюватиме, оскільки Djongo "перекладає" запит для MongoDB
    quotes = Quote.objects.all()
    return render(request, 'quotes/index.html', {'quotes': quotes})


def index(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/index.html', {'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def index(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/index.html', {'quotes': quotes})

def author_quotes(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    quotes = Quote.objects.filter(author=author)
    return render(request, 'quotes/author_quotes.html', {'author': author, 'quotes': quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})