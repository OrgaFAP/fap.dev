from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")  # type: ignore


def index2(request):
    return render(request, "website/index.html")


def donate(request):
    return render(request, "website/donate.html")


def analysis(request):
    today = date.today()
    days = [today - timedelta(days=i) for i in range(5)]
    return render(request, "website/analysis.html", {"days": days})


def ressource(request):
    return render(request, "website/ressource.html")


def thoughts(request):
    return render(request, "website/thoughts.html")


def why(request):
    return render(request, "website/why.html")


def how_data(request):
    return render(request, "website/how_data.html")
