from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from se_app.models import *
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import update_last_login
from rest_framework import status
import re
from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.core.mail import send_mail
from .constants import *

EMAIL_HOST_USER = settings.EMAIL_HOST_USER
#HOST = settings.FRONT_END_URL
SECRET_KEY = settings.SECRET_KEY

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):

    email=serializers.CharField(max_length=255,write_only=True)
    authToken = serializers.CharField(max_length=255,required=False)
    password = serializers.CharField(max_length=255,required=False)
    name=serializers.CharField(max_length=255,required=False)

    login_type = serializers.CharField(write_only=True)
    jwttoken = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        login_type = data.get("login_type", None)
    #    import pdb; pdb.set_trace()

        if login_type == 'FACEBOOK':
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
                User_Details.objects.create(email=email,name=name)   #authToken=auth_token
                data=User_Details.objects.filter(email=email).get()
                payload = JWT_PAYLOAD_HANDLER(data)
                jwt_token = JWT_ENCODE_HANDLER(payload)
            return {
                'email':email,
                'jwttoken': jwt_token
            }

        else:
            email=data.get("email",None)
            password=data.get("password",None)

            if (User_Details.objects.filter(email=email).exists()):
                user = User_Details.objects.filter(email=email).get()#,password=password).get()
            #    pass_word = user.password
            #    email = user.email

                #user = authenticate(email=email,password=password)
                #print(data)
            #    data=User_Details.objects.filter(email=email).get()

                if user is not None:
                #    login(data,user)
                    payload = JWT_PAYLOAD_HANDLER(user)
                    jwt_token = JWT_ENCODE_HANDLER(payload)
        #    user=User_Details.objects.filter(email=email).get()
        #    login_password=user.password
        #    if (password==login_password):
                    return{
                        'message':"login successfull",
                        'status_code': status.HTTP_200_OK,
                        'jwttoken':jwt_token
                        
                    }
                else:
                    return{
                        "message":"invlaid password",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    }
            else:
                return{
                    'message':'Invalid email or password',
                    'status_code': status.HTTP_400_BAD_REQUEST,
                }


        

# class ImageSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Card_Details
#         fields=('id',)

# class FormSerializers(serializers.ModelSerializer):
#     class Meta:
#         model=Card_Details
#         fields=('category','player_name','user','status','brand_name','card_number','certification'
#                 'certification_number','auto_grade','card_grade','year','autographed')

class CompleteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card_Details
        fields='__all__'

# class CompleteDataSerializerNew(serializers.ModelSerializer):
#     class Meta:
#         model=CardDetailsNew
        fields='__all__'

class FormdataSerializers(serializers.Serializer):

    card_id=serializers.IntegerField(required=False)
    category=serializers.IntegerField(write_only=True)
    player_name=serializers.CharField(max_length=255,write_only=True)
    #status=serializers.CharField(max_length=255,write_only=True)
    brand_name=serializers.CharField(max_length=255,write_only=True)
    card_number=serializers.CharField(max_length=255,write_only=True)
    certification=serializers.IntegerField(write_only=True)
    certification_number=serializers.CharField(max_length=255,write_only=True)
    auto_grade=serializers.CharField(max_length=255,required=False)
    card_grade=serializers.CharField(max_length=255,write_only=True)
    year=serializers.CharField(max_length=255,write_only=True)
    autographed=serializers.BooleanField(write_only=True,default=False)

    message = serializers.CharField(max_length=255, read_only=True)
    success = serializers.CharField(max_length=255, read_only=True)
    status_code = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):

        card_id = data.get("card_id", None)
        category = data.get("category", None)
        player_name = data.get("player_name",None)
        #status = data.get("status", None)
        brand_name = data.get("brand_name", None)
        card_number = data.get("card_number", None)
        certification = data.get("certification", None)
        auto_grade = data.get("auto_grade", None)
        card_grade = data.get("card_grade", None)
        year = data.get("year", None)
        certification_number = data.get("certification_number", None)
        autographed=data.get("autographed",None)
        try:
            if card_id == None:
                Card_Details.objects.create(category_id=category,card_grade_id=card_grade,player_name=player_name,brand_name=brand_name,
                                        card_number=card_number,certification_id=certification,certification_number=certification_number,
                                        year=year,auto_grade_id=auto_grade,autographed=autographed,status=True)

                return {
                    'message':"saved a new form data",
                    'success':True,
                    'status_code':status.HTTP_200_OK,
                }
            else:
                if(Card_Details.objects.filter(id=card_id).exists()):
                    data=Card_Details.objects.filter(id=card_id).get()
                    data.category_id=category
                    data.player_name=player_name
                #data.status=status
                    data.brand_name=brand_name
                    data.card_number=card_number
                    data.certification_id=certification
                    data.auto_grade_id=auto_grade
                    data.card_grade_id=card_grade
                    data.year=year
                    data.certification_number=certification_number
                    data.autographed=autographed
                    data.status=True
                    data.save()
                    return {    
                        'message':"Card uploaded successfully",
                        'success':True,
                        'status_code':status.HTTP_200_OK,
                    }

        except Exception as e:
            #print(str(e))
            return{
                'message':str(e),
                'success':False,
                'status_code':status.HTTP_400_BAD_REQUEST,

            }

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email)

class signupSerializer(serializers.Serializer):

    first_name=serializers.CharField(max_length=255,write_only=True)
    last_name=serializers.CharField(max_length=255,write_only=True)
    email=serializers.EmailField(write_only=True)
    password=serializers.CharField(max_length=255,write_only=True)

    message = serializers.CharField(max_length=255, read_only=True)
    success = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):

        first_name=data.get("first_name",None)
        last_name=data.get("last_name",None)
        email=data.get("email",None)
        password=data.get("password",None)

        regexp = re.compile(r'^(?=.{8,})(?=.*[A-Z])(?=.*[@#$%^&+*!=]).*$')
        try:
            if (User_Details.objects.filter(email=email).exists()):
                return {
                    'message':"email already exists..!!",
                    'success':False,
                }
            else:
                if regexp.search(password):
                
                    subject = 'Signup Verification'
                    link = static_var['url'] + '/account-verify?token=' + generate_confirmation_token(email)
                    message = ("Hello " + email  + ",\n\nPlease click on the following link to verify:\n")
                    email_send = send_mail(subject, message + link, EMAIL_HOST_USER, [email], fail_silently=False, )    
                    user = User_Details.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password)
                    user.save()
                    return {    
                        'message':"User registered successfully, Mail has been sent for verification",
                        'success':True,
                    #    'status_code':status.HTTP_200_OK,
                    }
                else:
                    raise serializers.ValidationError('At least 8 characters, 1 uppercase letter, 1 number & 1 symbol')
        except Exception as e:
            return {
                'message': str(e),
                'success' : False,
            }

def confirm_token(token, expiration=43200):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, max_age=expiration)
    except:
        return False
    return email

class verify_tokenserializer(serializers.Serializer):

    token = serializers.CharField(max_length=255, write_only=True)

    message = serializers.CharField(max_length=255, read_only=True)
    success = serializers.CharField(max_length=255, read_only=True)
    status_code = serializers.CharField(max_length=255, read_only=True)

    def validate(self,data):
        
        token = data.get("token",None)

        email = confirm_token(token)
        print(email)
        if not email:
            return{
                'message':'Invalid Token',
                'status_code':status.HTTP_404_NOT_FOUND,
                'success':False,
            }
        else:
            user = User_Details.objects.filter(email=email).get()
            user.is_verified = True
            user.save()
            return {    
                    'message':"Account verified successfully",
                    'success':True,
                    'status_code':status.HTTP_200_OK,
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

# class loginserializer(serializers.Serializer):

#     email=serializers.EmailField(write_only=True)
#     password=serializers.CharField(max_length=255,write_only=True)

#     message = serializers.CharField(max_length=255, read_only=True)
# #    success = serializers.CharField(max_length=255, read_only=True)
#     status_code = serializers.CharField(max_length=255, read_only=True)

#     def validate(self,data):

#     #    import pdb; pdb.set_trace()

#         email=data.get("email",None)
#         password=data.get("password",None)
        
#         if (User_Details.objects.filter(email=email).exists()):
#             user=authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)
#         #    user=User_Details.objects.filter(email=email).get()
#         #    login_password=user.password
#         #    if (password==login_password):
#                 return{
#                     'message':"login successfull",
#                     'status_code': status.HTTP_200_OK,
#                 }
#             else:
#                 return{
#                     "message":"invlaid password",
#                     "status_code": status.HTTP_400_BAD_REQUEST,
#                 }
#         else:
#             return{
#                 'message':'Invalid email or password',
#                 'status_code': status.HTTP_400_BAD_REQUEST,
#             }

class forgot_password_serializer(serializers.Serializer):

    email=serializers.EmailField(write_only=True)

    message = serializers.CharField(max_length=255, read_only=True)
#    success = serializers.CharField(max_length=255, read_only=True)
    status_code = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self,data):

        email=data.get('email',None)
        user = User_Details.objects.filter(email=email).exists()
        if not user:
            return{
                'message':'Sorry, this is not a registered email address. Please try again',
                'status_code':status.HTTP_404_NOT_FOUND,
            }
        try:
            user = User_Details.objects.filter(email=email).get()
            link = static_var['url'] + '/reset-password?token=' + generate_confirmation_token(user.email)
            if not link:
                return{
                    'message':'The link has expired. Please click on forgot password to generate a new link',
                    'status_code':status.HTTP_204_NO_CONTENT,
                }
            subject = 'Reset Password'
            message = ("Hello " + user.name + ",\n\nPlease click on the following link to reset your password:\n")
        #    email_send = send_mail(subject, message + link, EMAIL_HOST_USER, [user.email], fail_silently=False,)
            email_send = send_mail(subject, message + link, EMAIL_HOST_USER, [user.email], fail_silently=False,)
            return{
                'message':'Recovery email sent successfully',
                'status_code':status.HTTP_200_OK,
            }
            if not email_send:
                return{
                    'message':'Recovery Email Failed',
                    'status_code':status.HTTP_400_BAD_REQUEST,
                }
        except User_Details.DoesNotExist:
            return{
                'message':'Sorry, this is not a registered email address. Please try again',
                'email': user.email,
                'status_code':status.HTTP_400_BAD_REQUEST,
            }

class reset_password_serializer(serializers.Serializer):
    token = serializers.CharField(max_length=255,write_only=True)
    password = serializers.CharField(max_length=255,write_only=True)
    confirm_password = serializers.CharField(max_length=255,write_only=True)

    message = serializers.CharField(max_length=255, read_only=True)
#   success = serializers.CharField(max_length=255, read_only=True)
    status_code = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        token = data.get("token", None)
        password = data.get("password", None)
        confirm_password = data.get("confirm_password", None)

        regexp = re.compile(r'^(?=.{8,})(?=.*[A-Z])(?=.*[@#$%^&+*!=]).*$')

        email = confirm_token(token)
        print(email)
        if not email:
            return{
                'success':'False',
                'message':'Invalid Token.',
                'status_code': status.HTTP_403_FORBIDDEN,
                }
        try:
            user = User_Details.objects.filter(email=email).get()
            # user.set_password(password)
            if regexp.search(password):
                if password == confirm_password:
                    user.set_password(password)
    #                user.password=password
                    user.save()
                    return{
                        'message':'Password Changed Successfully.',
                        'status_code':status.HTTP_200_OK,
                    } 
            else:
                return{
                    'message':'Password details not matched.',
                    'status_code':status.HTTP_400_BAD_REQUEST,
                }
        except User.DoesNotExist:
            return{
                'message':'Password reset failed.',
                'status_code':status.HTTP_400_BAD_REQUEST,
            } 