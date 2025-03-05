from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')

def signup_view(request):
    return render(request, 'pages/auth/signup.html')


def signin_view(request):
    return render(request, 'pages/auth/signin.html')

def features(request):
    return render(request, 'pages/features.html')

def testimonials(request):
    return render(request, 'pages/testimonials.html')