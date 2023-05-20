from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Post
from .forms import SignUpForm, LogInForm, PostForm
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        # Create sign up form with the data sent in the POST request
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Bound and correct format for values
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()

    # This line is executed in the case of a GET request, pass empty form to template
    return render(request, 'sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('feed')
        
        # If we got here, then details not found in database
        messages.add_message(request, messages.ERROR, "Invalid username or password. Please try again.")

    # For GET request, we do these
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    # Remove _auth_user_id from the session
    logout(request)
    return redirect('home')

def feed(request):
    form = PostForm()
    posts = Post.objects.all()
    return render(request, "feed.html", {'form': form, 'posts': posts})

def new_post(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            current_user = request.user
            form = PostForm(request.POST, request.FILES) 
            # request.FILES is a dictionary-like object similar to request.POST
            # request.POST contains POST data, request.FILES contains file data we are sending
            if form.is_valid():
                title = form.cleaned_data.get('title')
                image = form.cleaned_data.get('image')
                body = form.cleaned_data.get('body')

                post = Post.objects.create(
                    author=current_user,
                    title=title,
                    image=image,
                    body=body
                )

                return redirect('feed')
            else:
                return render(request, 'feed.html', {'form': form}) # Form invalid so re-render the feed
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden() # Got here means GET request

