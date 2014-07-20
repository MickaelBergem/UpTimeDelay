from django.shortcuts import render

def display_homepage(request):
    """ Displaying the homepage """
    return render(request, 'Site/home.html')