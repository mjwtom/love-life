from django.shortcuts import render
from django.http import HttpResponse
from tinymce.models import HTMLField
from polls.models import Quesion

# Create your views here.


def index(request):
    question = Quesion()
    return HttpResponse('!!!welcome to the application!!!')
