from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, QuotesForm, AuthorForm
from .models import Tag, Author, Quotes
from .utils import get_mongodb
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# db = get_mongodb()
# Create your views here.


def main(request, page=1):
    # quotes = Quotes.objects.all()
    # db = get_mongodb()
    # quotes = db.quotes.find()
    quotes = Quotes.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotesapp/index.html', {"quotes": quotes_on_page})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:root')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:root')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})

    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuotesForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            choice_author_ids = request.POST.getlist('authors')
            for author_id in choice_author_ids:
                author = Author.objects.get(fullname=author_id)
                id = author.id
                new_quote.author_id = id
            new_quote = form.save()
            return redirect(to='quotesapp:root')
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, 'form': form, "authors": authors})

    return render(request, 'quotesapp/quote.html', {"tags": tags, "authors": authors, 'form': QuotesForm()})


def detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotesapp/detail.html', {"author": author})
