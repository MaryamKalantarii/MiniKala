from rest_framework import serializers
from accounts.models import CustomeUser


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser  
        fields = ['id', 'email']
