from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from se_app.models import *
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    email=serializers.CharField(max_length=255,write_only=True)
    authToken = serializers.CharField(max_length=255,write_only=True)
    name=serializers.CharField(max_length=255,write_only=True)

    jwttoken = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        name = data.get("name", None)
        auth_token = data.get("authToken", None)
        if(User_Details.objects.filter(email=email).exists()):
            data=User_Details.objects.filter(email=email).get()
            data.authToken=auth_token
            data.save()
            payload = JWT_PAYLOAD_HANDLER(data)
            jwt_token = JWT_ENCODE_HANDLER(payload)
           # update_last_login(None, user)
        else:
            User_Details.objects.create(email=email,authToken=auth_token,name=name)
            data=User_Details.objects.filter(email=email).get()
            payload = JWT_PAYLOAD_HANDLER(data)
            jwt_token = JWT_ENCODE_HANDLER(payload)
        return {
            'email':email,
            'jwttoken': jwt_token
        }

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model=Card_Details
        fields=('id','front_image','back_image')

class FormSerializers(serializers.ModelSerializer):
    class Meta:
        model=Card_Details
        fields=('category','player_name','userid','status','brand_name','card_number','certification'
                'certification_number','auto_grade','card_grade','year')

class CompleteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card_Details
        fields='__all__'