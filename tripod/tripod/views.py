from django.shortcuts import render


def not_available_404(request):
    return render(request, '404.html')


def permission_error(request):
    return render(request, 'permissionError.html')


def admin_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'admin_page.html', context)
