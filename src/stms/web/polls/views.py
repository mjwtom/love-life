from django.shortcuts import render
from django.http import HttpResponse
from tinymce.models import HTMLField

# Create your views here.


def index(request):
    contents = HTMLField()
    return HttpResponse(contents)
