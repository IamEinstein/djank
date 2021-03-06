from django.core.exceptions import ValidationError
from django.http.response import Http404
from redirect.models import Redirect, RedirectLink, ProtectLink
from django.shortcuts import render, redirect
from django.urls.exceptions import NoReverseMatch
from django.http import HttpResponse
from datetime import datetime
from django.views import View
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
        l1 = RedirectLink.objects.create(link=link1)
        l1.save()
        l2 = RedirectLink.objects.create(link=link2)
        l2.save()
        l3 = RedirectLink.objects.create(link=link3)
        l3.save()
        l4 = RedirectLink.objects.create(link=link4)
        l4.save()
        l5 = RedirectLink.objects.create(link=link5)
        l5.save()
        l6 = RedirectLink.objects.create(link=link6)
        l6.save()
        l7 = RedirectLink.objects.create(link=link7)
        l7.save()
        l8 = RedirectLink.objects.create(link=link8)
        l8.save()
        l9 = RedirectLink.objects.create(link=link9)
        l9.save()
        l10 = RedirectLink.objects.create(link=link10)
        l10.save()
        now = datetime.now()
        date = int(now.strftime("%d"))
        if date >= 22:
            link1 = l1.get_url2()
            link2 = l2.get_url2()
            link3 = l3.get_url2()
            link4 = l4.get_url2()
            link5 = l5.get_url2()
            link6 = l6.get_url2()
            link7 = l7.get_url2()
            link8 = l8.get_url2()
            link9 = l9.get_url2()
            link10 = l10.get_url2()
            print("ok")
        else:
            # Setting alternative url

            link1 = l1.get_url(request=request)
            link2 = l2.get_url(request=request)
            link3 = l3.get_url(request=request)
            link4 = l4.get_url(request=request)
            link5 = l5.get_url(request=request)
            link6 = l6.get_url(request=request)
            link7 = l7.get_url(request=request)
            link8 = l8.get_url(request=request)
            link9 = l9.get_url(request=request)
            link10 = l10.get_url(request=request)

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
        link = f"""http://{host}/redirect/{new_redirect.unique_id}
        <br>
        Show link - http://{host}/redirect/show/{new_redirect.unique_id}
        """
        return render(request, "redirect/link.html", context={"link1": f"http://{host}/redirect/{new_redirect.unique_id}", "link2": f"http://{host}/redirect/show/{new_redirect.unique_id}"})
        # return HttpResponse(link)


def redirect_link(request, id):
    try:
        url = RedirectLink.objects.get(unique_id=id)
    except (AttributeError, RedirectLink.DoesNotExist):
        raise Http404
    else:
        try:
            return redirect(url.link)
        except NoReverseMatch:
            return render(request, "redirect/close.html")


class ProtectLinkView(View):
    @staticmethod
    def get(request):
        return render(request, "redirect/protect.html")

    @staticmethod
    def post(request):
        link = request.POST['link']
        protected = ProtectLink.objects.create(link=link)
        return HttpResponse(f"""
        
        
         Link - http://{request.META['HTTP_HOST']}/protect/{protected.id}
         <br>
         
         Password - {protected.password}""")


# def see_link(request, id):
#     p_link = ProtectLink.objects.get(id=id)
def showlinks(request, id):
    try:
        curent_redirect = Redirect.objects.get(unique_id=id)
    except Redirect.DoesNotExist:
        raise Http404
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
        print(f"link10 - {link10}")
        link_list = [link1, link2, link3, link4, link5,
                     link6, link7, link8, link9, link10]
        return render(request, "redirect/show.html", context={"links": link_list})
