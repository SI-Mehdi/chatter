from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LogInForm
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

    # This line is executed in the case of a GET request
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
    return render(request, 'feed.html')
