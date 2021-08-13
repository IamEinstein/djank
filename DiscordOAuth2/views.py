from django.http import HttpResponse
import requests
from django.views import View
from django.shortcuts import redirect, render
import os
from server.models import User, Discord_Account
# Create your views here.
alt_url = "https://discord.com/api/oauth2/authorize?client_id=833908026267271179&redirect_uri=https%3A%2F%2Fdjango-bank.herokuapp.com%2Fdiscord%2F&response_type=code&scope=identify"
alt_url_2 = "https://discord.com/api/oauth2/authorize?client_id=833908026267271179&redirect_uri=https%3A%2F%2Fdjank-the-bank.herokuapp.com%2Fdiscord%2F&response_type=code&scope=identify"
real_url = "https://discord.com/api/oauth2/authorize?client_id=833908026267271179&redirect_uri=https%3A%2F%2Fdjank.herokuapp.com%2Fdiscord%2F&response_type=code&scope=identify"


class LoginView(View):
    def get(self, request):
        if isinstance(User.get_user(request=request), User):
            user = User.get_user(request=request)
            try:
                discord_account = Discord_Account.objects.get(user=user)
            except Discord_Account.DoesNotExist:
                return redirect(f"http://{request.META['HTTP_HOST']}/site/yourAccount?not_linked=true")
            else:
                code = request.GET.get("code")
                if code == None:
                    return redirect("https://discord.com/api/oauth2/authorize?client_id=833908026267271179&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fdiscord%2F&response_type=code&scope=identify")
                discord_account_details = discord_get_user(request, code)
                if discord_account_details == None:
                    return redirect("https://discord.com/api/oauth2/authorize?client_id=833908026267271179&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fdiscord%2F&response_type=code&scope=identify")
                if discord_account.discord_username[0:-5] == discord_account_details['username'] or discord_account.is_verified == True:
                    discord_account.discord_id = discord_account_details['id']
                    discord_account.is_verified = True
                    discord_account.save()
                else:
                    return HttpResponse("You have not linked your discord username")

            return redirect("main:account")
        return redirect("main:login")
# Getting the user


def discord_get_user(request, code: str):
    try:
        data = {

            "client_id": os.getenv('DJANK_CLIENT_ID'),
            "client_secret": os.getenv("DJANK_CLIENT_SECRET"),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:8000/discord/",
            "scope": "identify"
        }
        header = {"Content-type": 'application/x-www-form-urlencoded',
                  }
        response = requests.post(
            "https://discord.com/api/oauth2/token", data=data, headers=header)
        print(response)
        credentials = response.json()
        print(credentials)
        access_token = credentials['access_token']
        response = requests.get("https://discord.com/api/v6/users/@me", headers={

            "Authorization": f"Bearer {access_token}"
        }, )
        print(response)
        user = response.json()
        print(user)
        # avatar_url = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}"
        return user
    except KeyError:
        return None
