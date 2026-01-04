from django.http import HttpResponse

def home(request):
    return HttpResponse("Jonaki Machine Store is running successfully!")