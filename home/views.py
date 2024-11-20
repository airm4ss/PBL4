from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'home/main.html')

def generatorHave(request):
    return render(request, 'geneHave_home.html')

def generatorNo(request):
    return render(request, 'genNo_home.html')
