from django.shortcuts import render, HttpResponse


def landing_page(request):
    return HttpResponse("<h1>Hello, this is the landing page</h1>")
