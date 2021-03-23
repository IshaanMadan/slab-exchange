from django.shortcuts import render
from se_app.models import *
from se_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.http import HttpResponse
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import logout, login
from rest_framework.permissions import AllowAny,IsAuthenticated
from sport_backend import settings
from django.http import FileResponse
import os
from PIL import Image
import argparse
from pathlib import Path
import json
from django.core.files import File
from django.forms.models import model_to_dict
from django.contrib import messages
import jwt

class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):

        email=request.data['email']
        print(email)
        password=request.data['password']
        print(password)
        if (User_Details.objects.filter(email= email).exists()):
            user=User_Details.objects.filter(email = email).get()
            print(user)
     #        user=authenticate(user)
            login(request,user)
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
    #    login(request,)
        
            response = {
                'success' : 'True',
                'status_code' : status.HTTP_200_OK,
                'message': 'User logged in  successfully',
                'jwttoken' : serializer.data['jwttoken'],
             }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)


class ImageAPIVIEW(APIView):

    permission_classes = (IsAuthenticated,)
    
    def post(self,request):

        try:
        #     import pdb;pdb.set_trace()
            file_ref = request.FILES['image']
            file_name = file_ref.name
            row_id = request.GET.get('card_id')
        #    row_id = None if row_id == 'null' else int(row_id)
        
            file_ext = file_ref.name.split('.')[-1]
            is_front = bool(request.GET.get('front', False))

            print(is_front)
            ext=['jpg','jpeg','png']
            if file_ext not in ext:
                raise Exception("Invalid Format")

            if not row_id:
                if(is_front):
                    front_file_ref, back_file_ref = file_ref, None
                    front_thumbnail_path , back_thumbnail_path = create_thumbnail(is_front,file_ref), None
                else:
                    front_file_ref, back_file_ref = None, file_ref
                    front_thumbnail_path , back_thumbnail_path  = None, create_thumbnail(is_front,file_ref)                     
                
                detail_ref = Card_Details(front_image=front_file_ref, back_image=back_file_ref,front_thumbnail=front_thumbnail_path, back_thumbnail=back_thumbnail_path, user_id=request.user.id)
                detail_ref.save()

                back_thumbnail_path = detail_ref.back_thumbnail.url if detail_ref.back_thumbnail else None
                front_thumbnail_path = detail_ref.front_thumbnail.url if detail_ref.front_thumbnail else None
                res_dict = {
                    "id": detail_ref.id,
                    "user_id": detail_ref.user.id,
                    "back_thumbnail": back_thumbnail_path,
                    "front_thumbnail": front_thumbnail_path,
                }
                return Response({'data': res_dict, "message": "Image uploaded successfully", "success": True},status=status.HTTP_201_CREATED)    
            else:       
                if is_front:
                    front_file_ref, back_file_ref = file_ref, None
                    front_thumbnail_path , back_thumbnail_path = create_thumbnail(is_front,file_ref), None
                    detail_ref= Card_Details.objects.get(id=row_id)
                    detail_ref.front_image = front_file_ref
                    detail_ref.front_thumbnail = front_thumbnail_path
                #    detail_ref.user_id = request.user.id
                #    detail_ref.status = 0
                    detail_ref.save()
                    #detail_ref = Card_Details.objects.filter(id=row_id).update(front_image = front_file_ref,front_thumbnail = front_thumbnail_path, user_id=request.user.id)
                else:
                    front_file_ref, back_file_ref = None, file_ref
                    front_thumbnail_path , back_thumbnail_path  = None, create_thumbnail(is_front,file_ref)
                    detail_ref= Card_Details.objects.get(id=row_id)
                    detail_ref.back_image = back_file_ref
                    detail_ref.back_thumbnail = back_thumbnail_path
                #    detail_ref.status = 0
                    detail_ref.save()
                    #detail_ref = Card_Details.objects.filter(id=row_id).update(back_image=back_file_ref,back_thumbnail=back_thumbnail_path, user_id=request.user.id)
                back_thumbnail_path = detail_ref.back_thumbnail.url if detail_ref.back_thumbnail else None
                front_thumbnail_path = detail_ref.front_thumbnail.url if detail_ref.front_thumbnail else None
                res_dict = {
                    "id": detail_ref.id,
                    "user_id": detail_ref.user_id,
                    "back_thumbnail": back_thumbnail_path,
                    "front_thumbnail": front_thumbnail_path,
                }
                return Response({'data': res_dict, "message": "Image uploaded successfully", "success": True},status=status.HTTP_201_CREATED)
                
        except Exception as err:
            return Response({'data': None, "message": str(err), "success": False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_thumbnail(is_front, file_ref):
    image = Image.open(file_ref)
    file_name = file_ref.name
    MAX_SIZE = (175, 232) 
    image.thumbnail(MAX_SIZE)    
    thumbnail_dir_name = "front_thumbnails" if is_front else "back_thumbnails"
    final_path = os.path.join(settings.MEDIA_ROOT, thumbnail_dir_name, file_name)
    relative_path = os.path.join(thumbnail_dir_name, file_name)
    image.save(final_path)
    return relative_path

class DetailAPI(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get(self,request):

        statuses=request.GET['status']
        row_userid=request.user.id

        code_status=0
        if(statuses=='pending'):
            code_status=0
        else:
            code_status=1                 
                              ##status__status__exact
        if code_status==0:
            card=Card_Details.objects.filter(user_id=row_userid,status=code_status,is_deleted=0)
            print(card)
            serializers=CompleteDataSerializer(card,many=True)
            # if serializers.is_valid():
            #     serializers.save()
            return Response({'data':serializers.data},status=status.HTTP_201_CREATED)
        else:
            card=Card_Details.objects.filter(user_id=row_userid,status=code_status,is_deleted=0)
            serializers=CompleteDataSerializer(card,many=True)
            # if serializers.is_valid():
            #     serializers.save()
            return Response({'data':serializers.data,'message':'file fetched'}, status=status.HTTP_201_CREATED)

# class savecarddetails(APIView): Vignesh@1qaz
#     permission_classes = (IsAuthenticated,)
#     serializer_class = FormdataSerializers

#     def post(self,request):

#         card_id=request.GET.get('card_id')
#         userid=request.user.id
#         category = request.data["category"]
#         player_name = request.data["player_name"]
#         #status = data.get("status", None)
#         brand_name = request.data["brand_name"]
#         card_number = request.data["card_number"]
#         certification = request.data["certification"]
#         auto_grade = request.data["auto_grade"]
#         card_grade = request.data["card_grade"]
#         year = request.data["year"]
#         certification_number = request.data["certification_number"]
#         autographed=request.data["autographed"]

#         try:
#             if card_id==None:
#                 Card_Details.objects.create(category_id=category,card_grade_id=card_grade,player_name=player_name,brand_name=brand_name,
#                                         card_number=card_number,certification_id=certification,certification_number=certification_number,
#                                         year=year,auto_grade_id=auto_grade,autographed=autographed,status=True,user_id=userid,is_deleted=False)

#                 return  Response({
#                     'message':"saved a new form data",
#                     'success':True,
#                     'status_code':status.HTTP_200_OK,
#                 })
#             else:
#                 if Card_Details.objects.filter(id=card_id).exists():
#                     data=Card_Details.objects.filter(id=card_id).get()
#                     data.category_id=category
#                     data.player_name=player_name
#                  #data.status=status
#                     data.brand_name=brand_name
#                     data.card_number=card_number
#                     data.certification_id=certification
#                     data.auto_grade_id=auto_grade
#                     data.card_grade_id=card_grade
#                     data.year=year
#                     data.certification_number=certification_number
#                     data.autographed=autographed
#                     data.status=True
#                     data.is_deleted=False
#                     data.save()
#                 return Response({    
#                         'message':"Card uploaded successfully",
#                         'success':True,
#                         'status_code':status.HTTP_200_OK,
#                     })

#         except Exception as err:
#             return Response({
#                      'message': str(err),
#                      'success':False,
#                      'status_code':status.HTTP_400_BAD_REQUEST,

#              })
#         # print(request.data)
#         # print(request.user.id)
#         # card_id = request.data['card_id']
#         # if Card_Details.objects.filter(id=card_id).exists():
#         #     Card=Card_Details.objects.filter(id=card_id).get()
#         #     Card.user_id=request.user.id
#         #     Card.save()
#         #     print('ID',request.POST['card_id'])
#         #     print(request.data['card_id'])
#         #     print(request.data)
#         #     serializer = FormdataSerializers(data=request.data)
#         #     serializer.is_valid(raise_exception=True)
#         #     response = {
#         #     'success' : 'data added'#serializer.data['success'],
#         # #    'status_code' : serializer.data['status_code'],
#         # #    'message' : serializer.data['message'],    
#         #     }
#             return Response(response)

class getformlist(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get(self,request):

        category=Card_Category.objects.all()
        certification=Certifications.objects.all()
        card_grade=Cardgrade.objects.all()
        auto_grade=Autograde.objects.all()


        serializer1=categorySerializer(category,many=True)
        serializer2=CardgradeSerializer(card_grade,many=True)
        serializer3=certificationSerializer(certification,many=True)
        serializer4=AutogradeSerializer(auto_grade,many=True)

        response = {
                'message':"list fetched succcessfully",
                'data':[{'category' :serializer1.data,'card_grade' :serializer2.data,
                'certification':serializer3.data,'auto_grade':serializer4.data,
            }],
                'success':True

        }
        return Response(response,status=status.HTTP_200_OK) 
        
    
class Deletecard(APIView):

    permission_classes = (IsAuthenticated,)

    def delete(self,request,card_id):
        #card_id = request.data('card_id')
        messages.warning(request, 'Are you sure you want to delete ?')
        try:
            card=Card_Details.objects.filter(id=card_id).get()
            #final_path = os.path.join(settings.MEDIA_ROOT, thumbnail_dir_name, file)
            anonymous_user_id=card.user_id
            authenticate_user_id= request.user.id
            if(anonymous_user_id==authenticate_user_id):
                if(Card_Details.objects.filter(id=card_id).exists()):
                    Card = Card_Details.objects.filter(id=card_id).get()
                    Card.is_deleted = True
                    Card.save()
                # Card_Details.objects.filter(id=card_id).delete()
                    response={
                     'message':"Data delete succcessfully",
                     'status_code':status.HTTP_200_OK,
                     'success':True
                     }
                #return Response(response)
            else:
                response={
                    'message':"You are not Authorized for this Action ",
                    'status_code':status.HTTP_401_UNAUTHORIZED,
                    'success':False
                }
                #return Response(response)

        except Exception as e:
            response={
                    'message':"Data Not Found ",
                    'status_code':status.HTTP_400_BAD_REQUEST,
                    'success':False
                }
            #return Response(response)
        return Response(response)


class savecarddetails(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormdataSerializers

    def post(self,request):

        serializer = FormdataSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        Card=Card_Details.objects.filter(card_number=request.data['card_number']).get()
        Card.user_id=request.user.id
        Card.save()
        response = {
            'success' : serializer.data['success'],
            'status_code' : serializer.data['status_code'],
            'message' : serializer.data['message'],    
        }
        return Response(response)

class signup(APIView):

    permission_classes = (AllowAny,)
    serializer_class = signupSerializer

    def post(self, request):
        serializer = signupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            'success' : serializer.data['success'],
            'message' : serializer.data['message'],   
        }
        return Response(response)

class verifytoken(APIView):
    
    permission_classes = (AllowAny,)
    serializer_class = verify_tokenserializer

    def post(self, request):
        print(request.data)
        serializer = verify_tokenserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : serializer.data['success'],
            'message' : serializer.data['message'],
            'status_code' : serializer.data['status_code'], 
        }
        return Response(response)

# # class login(APIView):

# #     permission_classes = (IsAuthenticated,)
# #     serializer_class = loginserializer

# #     def post(self, request):
# #         serializer = loginserializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)
# #         login
# #         response = {
# #             'status_code' : serializer.data['status_code'],
# #             'message' : serializer.data['message'], 
# #         }
# #         return Response(response)

class forget_password(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = forgot_password_serializer

    def post(self, request):
        serializer = forgot_password_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response ={
            'status_code' : serializer.data['status_code'],
            'message' : serializer.data['message'], 
        }
        return Response(response)

class reset_password(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = reset_password_serializer

    def post(self, request):

        serializer = reset_password_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response ={
            'status_code' : serializer.data['status_code'],
            'message' : serializer.data['message'], 
        }
        return Response(response)

class logout(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
