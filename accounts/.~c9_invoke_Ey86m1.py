from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def signup(request):

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            r
