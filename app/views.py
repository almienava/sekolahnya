from django.shortcuts import render




def error_handler_500(request, exception=None):
    return render(request, '500.html',status=500)

def not_found_handler(request, exception=None):
    return render(request, '404.html', status=404)

def error_handler_403(request, exception=None):
    return render(request, '403.html',status=403)
