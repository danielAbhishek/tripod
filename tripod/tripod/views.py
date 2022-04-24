from django.shortcuts import render


def not_available_404(request):
    return render(request, '404.html')
