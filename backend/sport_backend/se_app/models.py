from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser

class login_types(models.Model):
    type=models.CharField(max_length=255)

    def __str__(self):
        return self.type

class User_Details(AbstractBaseUser):
    name=models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    login_type=models.ForeignKey(login_types,on_delete=models.CASCADE,default='1')
    authToken=models.CharField(max_length=255)


    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Card_Category(models.Model):
    sports=models.CharField(max_length=255)

    def __str__(self):
      return str(self.sports)

class Certifications(models.Model):
    certificates=models.CharField(max_length=255)

    def __str__(self):
      return str(self.certificates)

class Autograde(models.Model):
    auto_grade=models.CharField(max_length=255)

    def __str__(self):
      return str(self.auto_grade)

class Cardgrade(models.Model):
    card_grade=models.CharField(max_length=255)

    def __str__(self):
      return str(self.card_grade)

class Status(models.Model):
    status=models.CharField(max_length=7)

    def __str__(self):
      return str(self.status)

class Card_Details(models.Model):
    
    category=models.ForeignKey(Card_Category,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    player_name=models.CharField(max_length=255,blank=True,null=True)
    front_image=models.ImageField(upload_to='front_images',null=True,blank=True)
    upload_time=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    back_thumbnail=models.ImageField(upload_to='front_thumbnails',max_length=255,null=True, blank=True)
    front_thumbnail=models.ImageField(upload_to='back_thumbanils',max_length=255,null=True,blank=True)
    back_image=models.ImageField(upload_to='back_images',null=True,blank=True)
    user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)
    status=models.ForeignKey(Status,on_delete=models.CASCADE,max_length=7,null=True,blank=True)
    brand_name=models.CharField(max_length=255,null=True,blank=True)
    card_number=models.CharField(max_length=255,unique=True,null=True,blank=True)
    certification=models.ForeignKey(Certifications,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    certification_number=models.CharField(max_length=255,null=True,blank=True)
    auto_grade=models.ForeignKey(Autograde,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    card_grade=models.ForeignKey(Cardgrade,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    year=models.IntegerField(null=True,blank=True)
    autographed=models.BooleanField(null=True,blank=True)

# class CardDetailsNew(models.Model):
#     # front_image=models.ImageField(upload_to='front_images',null=True,blank=True)
#     user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)
