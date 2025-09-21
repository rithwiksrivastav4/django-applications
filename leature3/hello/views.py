from django.http import HttpResponse # type: ignore
from django.shortcuts import render # type: ignore

# Create your views here.
def index(request):
    return render(request,"hello/index.html")

def srivastav(request):
    return HttpResponse("hello srivastav")

def name(request):
    return HttpResponse("my name is bobby:")

def greet(request,name):
    return render(request, "hello/greet.html",{
                      "name": name.upper()
                  })
    
