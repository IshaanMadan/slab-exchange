from django.shortcuts import render
from se_app.models import *
from se_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.http import HttpResponse
from django.contrib.auth.signals import user_logged_in
from rest_framework.permissions import AllowAny
from sport_backend import settings
import os
from PIL import Image


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
        file_ext = file_ref.name.split('.')[-1]
        is_front = request.GET['front']
        row_id = request.GET['id']
        ext=['jpg','jpeg','png']
        if file_ext in ext:
            if row_id != None:
            #if request.data['id'].exists():
                if is_front == 'True':                               #.exists():
                    Card_Details.objects.filter(id = row_id).update(front_image = file_ref)
                    return Response({'id' : row_id,'data': file_ref})
                else:
                    Card_Details.objects.filter(id = row_id).update(back_image = file_ref)
                    return Response({'id' : row_id,'data' : file_ref})    
            else:       
                if is_front=='True':
                    Card_Details.objects.create(front_image = file_ref)
                    return Response({'data': file_ref})
                else:
                    Card_Details.objects.create(back_image = file_ref)
                    return Response({'data': file_ref})
               
        else:
            return Response({"message":"Error in File Format"},status=status.HTTP_403_FORBIDDEN)
               
class FormData(APIView):

    def post(self,request):
        details = request.data
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
