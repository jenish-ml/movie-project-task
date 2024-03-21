from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MovieForm
from .models import Movie, Review
from django.db.models import Q
from category.models import Category

def home(request):
    user = request.user
    movies = Movie.objects.all()
    query = request.GET.get('q')
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        movies = movies.filter(category__title=selected_category)
    if query:
        movies = movies.filter(Q(title__icontains=query) | Q(category__title__icontains=query))
    return render(request, 'index.html', {'user': user, 'movies': movies, 'categories': categories})

def add_movie(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('home')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form, 'categories': categories})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'view_movie.html', {'movie': movie, 'categories': Category.objects.all()})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.user == movie.added_by:
        movie.delete()
        messages.success(request, 'Movie deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this movie.')
    return redirect('home')

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid() and request.user == movie.added_by:
            form.save()
            messages.success(request, 'Movie updated successfully.')
            return redirect('home')
    else:
        form = MovieForm(instance=movie)
    categories = Category.objects.all()
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie, 'categories': categories})

def add_review(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review = Review(movie=movie, user=request.user, rating=rating, comment=comment)
        review.save()
        messages.success(request, 'Review added successfully.')
        return redirect('movie_detail', movie_id=movie_id)
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('home')
