from rest_framework import serializers
from django.contrib.auth.models import User 
from myapp.models import Cakebox

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)


    class Meta:
        model=User
        fields=["id","username","email","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class CakeboxSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    flavour=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    shape=serializers.CharField(read_only=True)

    class Meta:
        model=Cakebox
        fields="__all__"

