from django.shortcuts import render
from se_app.models import *
from se_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.http import HttpResponse
from django.contrib.auth.signals import user_logged_in
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


class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
            #import pdb;pdb.set_trace()
            file_ref = request.FILES['image']
            file_name = file_ref.name
            row_id = request.GET.get('card_id')
            row_id = None if row_id == 'null' else int(row_id)
        #    user=request.user.id
            #import pdb;pdb.set_trace()
            file_ext = file_ref.name.split('.')[-1]
            is_front = bool(request.GET.get('front', False))
        #    is_front = true
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
                
                detail_ref = Card_Details(front_image=front_file_ref, back_image=back_file_ref,front_thumbnail=front_thumbnail_path, back_thumbnail=back_thumbnail_path, user_id=request.user.id, status_id=1)
                detail_ref.save()
                # detail_ref = CardDetailsNew(user_id=request.user.id)
                # detail_ref.save()
                # serializer=FormSerializers(data=detail_ref , many=False )
                # serializer=CompleteDataSerializer(data=detail_ref.__dict__, many=False )
                # serializer.is_valid(raise_exception=True)
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
                    detail_ref.status_id = 1
                    detail_ref.save()
                    #detail_ref = Card_Details.objects.filter(id=row_id).update(front_image = front_file_ref,front_thumbnail = front_thumbnail_path, user_id=request.user.id)
                else:
                    front_file_ref, back_file_ref = None, file_ref
                    front_thumbnail_path , back_thumbnail_path  = None, create_thumbnail(is_front,file_ref)
                    detail_ref= Card_Details.objects.get(id=row_id)
                    detail_ref.back_image = back_file_ref
                    detail_ref.back_thumbnail = back_thumbnail_path
                    detail_ref.status_id = 1
                    detail_ref.save()
                    #detail_ref = Card_Details.objects.filter(id=row_id).update(back_image=back_file_ref,back_thumbnail=back_thumbnail_path, user_id=request.user.id)
                back_thumbnail_path = detail_ref.back_thumbnail.url if detail_ref.back_thumbnail else None
                front_thumbnail_path = detail_ref.front_thumbnail.url if detail_ref.front_thumbnail else None
                res_dict = {
                    "id": detail_ref.id,
                    "user_id": detail_ref.user.id,
                    "back_thumbnail": back_thumbnail_path,
                    "front_thumbnail": front_thumbnail_path,
                }
                return Response({'data': res_dict, "message": "Image uploaded successfully", "success": True},status=status.HTTP_201_CREATED)
                
        except Exception as err:
            return Response({'data': None, "message": str(err), "success": False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def create_thumbnail(is_front, file_ref):
    image = Image.open(file_ref)
    file_name = file_ref.name
    MAX_SIZE = (100, 100) 
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
        #import pdb;pdb.set_trace()
        print(row_userid)
        #print(row_request.user)
        code_status=0
        if(statuses=='pending'):
            code_status=1
        else:
            code_status=2                 
                              ##status__status__exact
        if code_status==1:
            card=Card_Details.objects.filter(user_id=row_userid,status_id=code_status)
            serializers=CompleteDataSerializer(card,many=True)
            # if serializers.is_valid():
            #     serializers.save()
            return Response({'data':serializers.data},status=status.HTTP_201_CREATED)
        else:
            card=Card_Details.objects.filter(user_id=row_userid,status_id=code_status)
            serializers=CompleteDataSerializer(card,many=True)
            # if serializers.is_valid():
            #     serializers.save()
            return Response({'data':serializers.data,'message':'file fetched'}, status=status.HTTP_201_CREATED)

class savecarddetails(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FormdataSerializers

    def post(self,request):

        print(request.data)
        serializer = FormdataSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : serializer.data['success'],
            'status_code' : serializer.data['status_code'],
            'message' : serializer.data['message'],    
        }
        return Response(response)

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
        try:
            #import pdb;pdb.set_trace()
            card=Card_Details.objects.filter(id=card_id).get()
            #final_path = os.path.join(settings.MEDIA_ROOT, thumbnail_dir_name, file)
            anonymous_user_id=card.user_id
            authenticate_user_id= request.user.id
            if(anonymous_user_id==authenticate_user_id):
            # if(Card_Details.objects.filter(id=card_id).exists()):
                Card_Details.objects.filter(id=card_id).delete()
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