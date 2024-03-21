from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm
from django.contrib.auth import login, logout
from .forms import UserRegistrationForm,UpdateUserForm
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from movie_management.models import Movie
from category.models import Category

def register(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        movies = Movie.objects.all()
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return render(request, 'register.html', {'form': form})
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            customer = CustomUser(user=user)
            customer.save()
            login(request, user)
            return render(request, 'index.html', {'form': form,'movies':movies,'categories': categories, 'alert':True})
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form, 'categories': categories})

def user_login(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            messages.success(request, 'Your Registration successful. Please Login!')
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'categories': categories})

def user_logout(request):
    logout(request)
    return redirect('home')

def view_profile(request):
    user = request.user
    categories = Category.objects.all()
    return render(request, 'view_profile.html', {'user': user, 'categories': categories})

def edit_profile(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            if password:
                user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form, 'categories': categories})
