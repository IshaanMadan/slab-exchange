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
        fields=('id',)

class FormSerializers(serializers.ModelSerializer):
    class Meta:
        model=Card_Details
        fields=('category','player_name','user','status','brand_name','card_number','certification'
                'certification_number','auto_grade','card_grade','year','autographed')

class CompleteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card_Details
        fields='__all__'

# class CompleteDataSerializerNew(serializers.ModelSerializer):
#     class Meta:
#         model=CardDetailsNew
        fields='__all__'

class FormdataSerializers(serializers.Serializer):

    row_id=serializers.IntegerField(write_only=True)
    category=serializers.IntegerField(write_only=True)
    player_name=serializers.CharField(max_length=255,write_only=True)
    status=serializers.CharField(max_length=255,write_only=True)
    brand_name=serializers.CharField(max_length=255,write_only=True)
    card_number=serializers.CharField(max_length=255,write_only=True)
    certification=serializers.IntegerField(write_only=True)
    certification_number=serializers.CharField(max_length=255,write_only=True)
    auto_grade=serializers.CharField(max_length=255,write_only=True)
    card_grade=serializers.CharField(max_length=255,write_only=True)
    year=serializers.CharField(max_length=255,write_only=True)

    message = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):
        row_id = data.get("id", None)
        category = data.get("category", None)
        player_name = data.get("player_name",None)
        status = data.get("status", None)
        brand_name = data.get("brand_name", None)
        card_number = data.get("card_number", None)
        certification = data.get("certification", None)
        auto_grade = data.get("auto_grade", None)
        card_grade = data.get("card_grade", None)
        year = data.get("year", None)
        certification_number = data.get("certification_number", None)

        if(Card_Details.objects.filter(id=row_id).exists()):
            data=Card_Details.objects.filter(id=row_id).get()
            data.category=category
            data.player_name=player_name
            data.status=status
            data.brand_name=brand_name
            data.card_number=card_number
            data.certification=certification
            data.auto_grade=auto_grade
            data.card_grade=card_grade
            data.year=year
            data.certification_number=certification_number
            data.save()
            return {
            'message':"updated form data"
            }
        else:
            return{
            'message':"id is not present"
            }

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Card_Category
        fields = '__all__'

class CardgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardgrade
        fields = '__all__'

class certificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certifications
        fields = '__all__'

class AutogradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autograde
        fields = '__all__'