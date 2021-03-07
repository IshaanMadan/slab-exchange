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


class UserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'jwttoken' : serializer.data['jwttoken'],
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class ImageAPIVIEW(APIView):

    def post(self,request):

        file_ref = request.FILES['image']
        file_name = file_ref.name
        row_id = request.GET.get('id')

        file_ext = file_ref.name.split('.')[-1]
        is_front = request.GET['front']
        ext=['jpg','jpeg','png']
        if file_ext in ext:
            image = Image.open(file_ref)
            MAX_SIZE = (500,500)
            image.thumbnail(MAX_SIZE)

            file_path='media/thumbnails/'+file_name
            image.save(file_path)
            img = open(file_path, 'rb')
            response = FileResponse(img)
            thumbnail = response.file_to_stream.name

            if row_id != None:
                if is_front == 'True':                               
                    Card_Details.objects.filter(id = row_id).update(front_image = file_ref ,front_thumbnail = thumbnail)
                    return Response({'id' : row_id,'front_image_thumbnail': file_path})
                else:
                    Card_Details.objects.filter(id = row_id).update(back_image = file_ref,back_thumbnail = thumbnail)
                    return Response({'id' : row_id,'back_image_thumbnail': file_path})    
            else:       
                if is_front=='True':
                    Card_Details.objects.create(front_image = file_ref.name,front_thumbnail = thumbnail)
                    return Response({'data': file_ref.name,'front_image_thumbnail': file_path})
                else:
                    Card_Details.objects.create(back_image = file_ref.name,back_thumbnail = thumbnail)
                    return Response({'data': file_ref.name,'back_image_thumbnail': file_path})
               
        else:
            return Response({"message":"Error in File Format"},status=status.HTTP_403_FORBIDDEN)

class FormData(APIView):

    def post(self,request):
        details = request.data['']
        category = request.data['category']
        player_name = request.data['player_name']
        userid = request.data['userid']
        status = request.data['status']
        brand_name = request.data['brand_name']
        card_number = request.data['card_number']
        certification = request.data['certification']
        certification_number = request.data['certification_number']
        auto_grade = request.data['auto_grade']
        card_grade = request.data['card_grade']
        year = request.data['year']
        Card_Details.object.filter(id=request.data['id']).update
        serializer = FormSerializers(data=details)
        if serializer.is_valid():
            serializer.save()
        return Response({"data":serializer.data,"messgae":"successful"},status=status.HTTP_201_CREATED)

    def get(self,request,pk):
        data=ImageDetails.objects.get(id=pk)
        serializers=CompleteDataSerializer(data)
        return Response({'data':serializer.data,'message':'file fetched'}, status=status.HTTP_201_CREATED)


class CompleteData(APIView):

    def get(self,request):
        data=ImageDetails.objects.all()
        serializers=CompleteDataSerializer(data,many=True)
        return Response({'data':serializer.data,'message':'file fetched'}, status=status.HTTP_201_CREATED)