from django.db.models.expressions import ExpressionList
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .mail import *
from .check import *
from .models import *
from django.db.utils import IntegrityError
from django.http import Http404
from django.views import View
from server.models import User
import uuid
import bcrypt


class MailView(View):
    def get(self, request):
        check_if_key_is_valid(Query)
        return render(request, 'mail/index.html')

    def post(self, request):
        check_if_key_is_valid(Query)
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect(f"http://{request.META['HTTP_HOST']}/mail?invalid=true")
        else:
            email = user.email
            if email != None and email.isspace() == False:
                if user.email_is_verified == True:
                    id = Query.objects.create(user=user, mail=user.email)
                    send__mail(id, user.email, request, user)
                    return render(request, "mail/sent.html")
                return redirect(f"http://{request.META['HTTP_HOST']}/mail?not_verified=true")
            else:
                return redirect(f"http://{request.META['HTTP_HOST']}/mail?mail_invalid=true")


class ResetPasswordView(View):
    def get(self, request, id1, id2):
        try:
            id1 = uuid.UUID(id1)
            id2 = uuid.UUID(id2)
            query = Query.objects.get(unique_id=id1)
        except (Query.DoesNotExist, AttributeError, TypeError):
            raise Http404
        else:
            if query.unique_id_2 == id2:
                user = query.user
                return render(request, "mail/reset_pwd.html", {"user": user})
            raise Http404

    def post(self, request):
        new_pwd = request.POST['new_password']
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        else:
            hash_pwd = bcrypt.hashpw(
                bytes(new_pwd, 'utf-8'), bcrypt.gensalt())
            user.password = hash_pwd
            user.save()
            try:
                query = Query.objects.get(user=user)
            except Query.DoesNotExist:
                return render(request, "error.html", context={'error': "Username not correct"})
            query.delete()
            return render(request, "mail/done.html")


class VerifyMail(View):
    def get(self, request, id):
        try:
            user = User.objects.get(unique_id=uuid.UUID(id))
        except (User.DoesNotExist):
            print("UUID NOT FOUND")
            return HttpResponse("NOT FOUND")
        else:
            if user.email_is_verified == False and user.email.isspace() == False and user.email != "":
                user.email_is_verified = True
                user.save()
                return render(request, "mail/verified.html")
            raise Http404
