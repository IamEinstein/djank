from django.core.exceptions import ValidationError
from redirect.models import Redirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
# Create your views here.


def index(request):
    return redirect('main:login')


def error_404(request, exception):
    error = "PAGE NOT FOUND"
    return render(request, "error.html", context={"error": error})


def server_error(request, exception=None):
    return render(request, "server_error.html", {})


def link(request):
    return render(request, "redirect/main.html")


def redirect_pg(request, id):
    try:
        curent_redirect = Redirect.objects.get(unique_id=id)
    except (Redirect.DoesNotExist, ValidationError, AttributeError, TypeError):
        return HttpResponse("DOES NOT EXIST")
    else:
        link1 = curent_redirect.link1
        link2 = curent_redirect.link2
        link3 = curent_redirect.link3
        link4 = curent_redirect.link4
        link5 = curent_redirect.link5
        link6 = curent_redirect.link6
        link7 = curent_redirect.link7
        link8 = curent_redirect.link8
        link9 = curent_redirect.link9
        link10 = curent_redirect.link10
        link_list = [link1, link2, link3, link4, link5,
                     link6, link7, link8, link9, link10]
        return render(request, "redirect/redirect.html", context={"links": link_list})
        # return redirect(link1)


def create_link(request):
    if request.method == "POST":
        link1 = request.POST.get('link1')
        link2 = request.POST.get('link2')
        link3 = request.POST.get('link3')
        link4 = request.POST.get('link4')
        link5 = request.POST.get('link5')
        link6 = request.POST.get('link6')
        link7 = request.POST.get('link7')
        link8 = request.POST.get('link8')
        link9 = request.POST.get('link9')
        link10 = request.POST.get('link10')
        r_list = [link1, link2, link3, link4, link5,
                  link6, link7, link8, link9, link10]
        host = request.META['HTTP_HOST']
        # print(r_list)
        # link = f"http://{host}/redirect?link1={link1}&link2={link2}&link3={link3}&link4={link4}&link5={link5}&link6={link6}&link7={link7}&link8={link8}&link9={link9}&link10={link10}"
        new_redirect = Redirect.objects.create(
            link1=link1,
            link2=link2,
            link3=link3,
            link4=link4,
            link5=link5,
            link6=link6,
            link7=link7,
            link8=link8,
            link9=link9,
            link10=link10,

        )
        link = f"http://{host}/redirect/{new_redirect.unique_id}"
        return HttpResponse(link)