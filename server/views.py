import bcrypt
from .errors import *
from django.core.exceptions import ValidationError
from django.http.response import Http404, HttpResponse
from .discord import *
from django.shortcuts import redirect, render
from .models import *
from .gen import *
from django.views import View
from mail.mail import *
# Create your views here.


class IndexView(View):
    def get(self, request):
        if isinstance(User.get_user(request=request), User):
            user = User.get_user(request=request)
            friends = user.get_friends()
            # if user.warned_email == False and user.email:

            return render(request, 'main/index.html', context={"user": user, "friends": friends})
        return User.get_user(request=request)


class LoginView(View):
    def get(self, request):
        try:
            request.COOKIES['user-identity']
        except KeyError:
            return render(request, 'main/login.html')
        else:
            return redirect("main:index")


class SignedUpView(View):
    def post(self, request):
        try:
            request.COOKIES['user-identity']
        except KeyError:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST.get('email')
            name = request.POST['name']
            discord_username = request.POST['discord_username']
            if User.objects.filter(username=username).exists() == True:
                return render(request, "main/signup.html", context={'error': "Username has already been taken"})
            if len(password) < 8:
                return render(request, "main/signup.html", context={'error': "Password should be atleast 8 characters long"})
            hash_pwd = bcrypt.hashpw(
                bytes(password, 'utf-8'), bcrypt.gensalt())
            name = name.capitalize()

            new_user = User.objects.create(

                username=username, password=hash_pwd, name=name)
            if email.isspace() == False and email != "":
                new_user.email = email
                new_user.save()
            response = render(request, 'main/logout.html',
                              context={"title": "Sign up", "text": "Creating your account"})
            response.set_cookie("user-identity", str(new_user.unique_id))
            if discord_username != "" and discord_username.isspace() == False:
                check = format_is_correct(discord_username)
                if check == None or check == "Blank Username":
                    response.set_cookie(
                        "discord_account", "None")
                else:
                    response.set_cookie(
                        "discord_account", "True")
                    new_discord_ac = Discord_Account.objects.create(
                        user=new_user, discord_username=discord_username)
            return response
        else:
            return redirect("main:index")

    def get(self, request):
        raise Http404


def signup(request):
    try:
        request.COOKIES['user-identity']
    except KeyError:
        return render(request, 'main/signup.html')
    else:
        return redirect("main:index")


class LoggedInView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() == True:
            user = User.objects.get(username=username)
            return user.authenticate(password, request)
        return render(request, "main/login.html", context={'error': "There is no account associated with this username"})

    def get(self, request):
        raise Http404()


def logout(request):
    return User.logout(request=request)


def add(request):
    if request.method == "POST":
        money_to_add = request.POST['add_amount']
        id = request.COOKIES['user-identity']
        user = User.objects.get(unique_id=id)
        try:
            user.bank_balance += int(money_to_add)
            user.save()
            new_transaction_created = Transaction(
                user=user, amount=money_to_add, type="add")
            user.transaction(new_transaction_created)
        except ValueError:
            return render(request, "error.html", context={"error": "How can u add a non-number field to your bank balance ?"})
        return redirect("main:index")
    return render(request, "error.html", context={"error": "Access Denied"})


def withdraw(request):
    if request.method == "POST":
        money_to_withdraw = request.POST['withdraw_amount']
        id = request.COOKIES['user-identity']
        user = User.objects.get(unique_id=id)
        try:
            money_to_withdraw = int(money_to_withdraw)
        except ValueError:
            return render(request, "error.html", context={"error": "How can u withdraw a non-number field to your bank balance ?"})

        if int(money_to_withdraw) > user.bank_balance:
            return render(request, "error.html", context={"error": "How can your withdraw amount be greater than your bank balance"})
        user.bank_balance -= int(money_to_withdraw)
        user.save()
        new_transaction_created = Transaction(
            user=user, amount=money_to_withdraw, type="withdraw")
        user.transaction(new_transaction_created)
        return redirect("main:index")
    return render(request, "error.html", context={"error": "Access Denied"})


def del_account(request):
    if request.method == "POST":
        if isinstance(User.get_user(request=request), User):
            user = User.get_user(request=request)
            user.delete()
            res = render(request, "main/logout.html",
                         context={"text": "Deleting your account"})
            res.delete_cookie("user-identity")
            return res
        return User.get_user(request=request)
    else:
        return HttpResponse("ACCESS DENIED")


def account(request):
    if isinstance(User.get_user(request=request), User):
        user = User.get_user(request=request)
        try:
            discord_account = Discord_Account.objects.get(user=user)
        except Discord_Account.DoesNotExist:
            if user.email == None:
                return render(request, "main/account.html", context={"user": user, "warning": warning})
            if user.email_is_verified == False:
                return render(request, "main/account.html", context={"user": user, "warning2": warning2})
            return render(request, "main/account.html", context={"user": user})
        else:

            if user.email == None:
                # if discord_account.is_verified == True:
                return render(request, "main/account.html", context={"user": user, "discord_account": discord_account, "warning": warning})
                # elif discord_account.is_verified == False:
                # return render(request, "main/account.html", context={"user": user, "discord_account": discord_account, "warning": warning, "not_verified":True})

            if user.email_is_verified == False:
                return render(request, "main/account.html", context={"user": user,  "discord_account": discord_account, "warning2": warning2})
            return render(request, "main/account.html", context={"user": user, "discord_account": discord_account})

    else:
        return User.get_user(request)


def change_pwd(request):
    if isinstance(User.get_user(request=request), User):
        user = User.get_user(request=request)
        if request.method == "GET":
            return HttpResponse("Access Denied")
        if request.method == "POST":
            pwd = request.POST['password']
            hash_pwd = bcrypt.hashpw(
                bytes(pwd, 'utf-8'), bcrypt.gensalt())
            user.password = hash_pwd
            user.save()

            host = request.META['HTTP_HOST']
            return redirect(f"http://{host}/site/yourAccount?pwd_change=true")
    else:
        return User.get_user(request=request)


# Transaction list for user
def transaction_list(request):
    if isinstance(User.get_user(request=request), User):
        user = User.get_user(request=request)
        try:
            transaction_list = user.get_transactions()
        except TypeError:
            return render(request, "main/transactions.html", context={"no_t": "You have no transactions"})
        return render(request, "main/transactions.html", context={"transactions": transaction_list, "host": request.META['HTTP_HOST']})
    return User.get_user(request=request)


def delete_transaction_history(request):
    if isinstance(User.get_user(request=request), User):
        if request.method == "POST":
            user = User.get_user(request=request)
            user.transaction_list = []
            user.save()
            host = request.META['HTTP_HOST']
            return redirect(f"http://{host}/site/yourAccount?t_list_erase=true")
        return HttpResponse("Access Denied")


def transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        user = transaction.user
        return render(request, "main/transaction.html", context={"transaction": transaction, "user": user})
    except (Transaction.DoesNotExist, KeyError, ValidationError):
        return HttpResponse("Invalid ID")


class LinkDiscordView(View):
    def post(self, request):
        user = User.get_user(request=request)
        discord_username = request.POST['username']
        if format_is_correct(discord_username) != "Blank Username" and format_is_correct(discord_username) != None:
            new_discord_account = Discord_Account.objects.create(
                discord_username=discord_username, user=user)
            new_discord_account.save()
            host = request.META['HTTP_HOST']
            return redirect(f"http://{host}/site/yourAccount?discord_account_linked=true")
        host = request.META['HTTP_HOST']
        return redirect(f"http://{host}/site/yourAccount?format_incorrect=true")


class UnlinkDiscordView(View):
    def post(self, request):
        user = User.get_user(request=request)

        try:
            new_discord_account = Discord_Account.objects.get(user=user)
            new_discord_account.delete()
        except (Discord_Account.DoesNotExist):
            pass
        host = request.META['HTTP_HOST']
        return redirect(f"http://{host}/site/yourAccount?discord_account_unlinked=true")


# FRIENDS
class FriendsView(View):
    def get(self, request):
        if isinstance(User.get_user(request=request), User):
            user = User.get_user(request=request)
            return render(request, "main/friends.html", context={"friends": user.get_friends()})
        return User.get_user(request=request)


class AddFriends(View):
    def get(self, request):
        if isinstance(User.get_user(request=request), User):
            user = User.get_user(request=request)
            return render(request, "main/add_friends.html", context={"user": user})
        return User.get_user(request=request)

    def post(self, request):
        friend_username = request.POST['friend']
        try:
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            return redirect(f"http://{request.META['HTTP_HOST']}/site/addFriends?doesnotexist=true")
        else:
            current_user = User.get_user(request=request)
            current_user.add_friend(friend.username)
            return redirect(f"http://{request.META['HTTP_HOST']}/site/addFriends?added=true")


# Money transferring
class TransferView(View):
    def get(self, request):
        raise Http404

    def post(self, request):
        amount = request.POST['amount']
        recipient_username = request.POST['username']
        sender = User.get_user(request=request)
        recipient = User.objects.get(username=recipient_username)
        try:
            amount = int(amount)
        except (ValueError, TypeError):
            return render(request, "error.html", context={"error": "You cant transfer something other than money"})

        recipient.bank_balance += int(amount)
        if sender.bank_balance < int(amount):
            return redirect(f"http://{request.META['HTTP_HOST']}/site/index?transfer_form=true&amount_less=true")
        sender.bank_balance -= int(amount)
        recipient.save()
        sender.save()
        return redirect(f"http://{request.META['HTTP_HOST']}/site/index?transferred=true")


# Add email
class AddEmailView(View):
    def get(self, request):
        if isinstance(User.get_user(request=request), User):
            user = User.get_user(request=request)
            user.email = None
            user.email_is_verified = False
            user.save()
            return redirect("main:account")
        return User.get_user(request=request)

    def post(self, request):
        email = request.POST['email']
        user = User.get_user(request=request)
        user.email = email
        user.save()
        verifymail(email)
        send_verify_mail(email, request, user)
        return redirect(f"http://{request.META['HTTP_HOST']}/site/index?email_added=true")
