#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.


def hp(request):
    return render(request, 'tramino/hp.html')
