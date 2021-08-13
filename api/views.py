from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from server.models import *
from .serializers import *
from rest_framework.views import APIView
from bank.settings import SECRET_KEY


class LoginAPIView(APIView):
    serializer_class = BotLoginSerializer

    # def get(self, request, format=None):
    #     return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Not found"})

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            bot_key = serializer.data.get("bot_key")
            if bot_key == SECRET_KEY:
                username = serializer.data.get("username")
                try:
                    user = User.objects.get(username=username)
                except (User.DoesNotExist, TypeError):
                    return Response(data={"error": "No user found"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    try:
                        discord_account = Discord_Account.objects.get(
                            user=user)
                    except Discord_Account.DoesNotExist:
                        return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Not linked"})
                    if discord_account.is_verified == False:
                        return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Account not verified"})
                    return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)

            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "error"})
        print("INVALID FORM")
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetBalanceAPIView(APIView):
    def post(self, request, format=None):
        pass


# class BotLoginAPIView(APIView):
#     serializer_class = BotLoginSerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             bot_key = serializer.data.get('bot_key')
#             if bot_key == SECRET_KEY:
#                 username = serializer.data.get('username')
#                 try:
#                     user = User.objects.get(username=username)
#                 except User.DoesNotExist:
#                     return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "User does not exist"})
#                 else:
#                     pwd = serializer.data.get('password')
#                     # if user.authenticate(pwd, request, bot=True):
#                     if True:
#                         discord = serializer.data.get('discord_username')
#                         try:
#                             discord_ac = Discord_Account.objects.get(
#                                 discord_username=discord, user=user)
#                         except Discord_Account.DoesNotExist:
#                             return Response(data={"error": "This discord account has not been linked"}, status=status.HTTP_400_BAD_REQUEST)
#                         else:
#                             d_user = discord_ac.user
#                             if d_user.unique_id == user.unique_id:
#                                 discord_ac.is_verified = True
#                                 discord_ac.save()
#                             else:
#                                 return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"error": "Your discord account in the site and request dont match"})

#                     return Response(status=status.HTTP_200_OK, data=UserSerializer(user).data)
#             else:
#                 return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "Request  Source is not verified"})
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={"error": "GET request is not allowed"})


# class BotLoginView(APIView):
#     serializer_class =BotLoginSerializer
#     def post(self, request, format):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             bot_key = serializer.data.get("bot_key")
#             if bot_key==SECRET_KEY:
#                 try:
#                     user
#             else:
#                 return Response(status=status.HTTP_403_FORBIDDEN, data={"error":"source not verified"})

#
#
#
#
#
#
#
#
#
# ?  PREVIOUS API VIEWS WHICH ARE NO LONGER NEEDED
# class UserView(generics.ListAPIView):
    #     queryset = User.objects.all()
    #     serializer_class = UserSerializer

# class TestAPIView(APIView):
#     serializer_class = Discord_AccountSerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user_id = serializer.data.get('user')
    #             user = User.objects.get(id=user_id)
    #             return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
