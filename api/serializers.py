from django.db import models
from rest_framework import serializers
from server.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'bank_balance', 'name', 'unique_id')


class BotLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    id = serializers.IntegerField()
    bot_key = serializers.CharField(max_length=200)
    discord_username = serializers.CharField(max_length=40)


class BotBalanceSerializer(serializers.Serializer):
    bot_key = serializers.CharField(max_length=200)
    discord_username = serializers.CharField(max_length=40)


class BotTransactionSerializer(serializers.Serializer):
    bot_key = serializers.CharField(max_length=200)
    discord_username = serializers.CharField(max_length=40)
    amount = serializers.FloatField()
    type = serializers.CharField(max_length=100)

    def check_type(self):
        if self.type == "add" or self.type == "withdraw":
            return True
        return False
