from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')

def signup_view(request):
    return render(request, 'pages/auth/signup.html')


def signin_view(request):
    return render(request, 'pages/auth/signin.html')