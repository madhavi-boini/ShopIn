from email import message
from django.shortcuts import render



def page404(request, exception):
    return render(request, 'page404.html')

