#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    return render(request, 'tramino/index.html')

def mypage(request):
    return render(request, 'tramino/mypage.html')

def match_search(request):
    return render(request, 'tramino/match_search.html')

def match_detail(request):
    return render(request, 'tramino/match_detail.html')

def event_post(request):
    return render(request, 'tramino/event_post.html')

def team_search(request):
    return render(request, 'tramino/team_search.html')

def team_detail(request):
    return render(request, 'tramino/team_detail.html')

def login(request):
    return render(request, 'tramino/login.html')

def create(request):
    return render(request, 'tramino/create.html')
