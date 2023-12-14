from django.shortcuts import render
from django.shortcuts import redirect


def landing_page(request):
    # is user is authenticated, redirect to home page
    if request.user.is_authenticated:
        return redirect("authuser:home")
    return render(request, "pages/landing_page.html")
