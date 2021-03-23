from django.db import models
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class login_types(models.Model):
    type=models.CharField(max_length=255)

    def __str__(self):
        return self.type
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('Users Must Have an email address')
        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, full_name, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model(full_name=full_name,email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User_Details(AbstractBaseUser,PermissionsMixin):
    full_name=models.CharField(max_length=255,blank=True)
    name=models.CharField(max_length=30)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    password=models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    login_type=models.ForeignKey(login_types,on_delete=models.CASCADE,default='1')
    authToken=models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects=UserManager()

    def __str__(self):
        return self.email

class Card_Category(models.Model):
    category_name=models.CharField(max_length=255)

    def __str__(self):
      return str(self.category_name)

class Certifications(models.Model):
    certificate_name=models.CharField(max_length=255)

    def __str__(self):
      return str(self.certificate_name)

class Autograde(models.Model):
    grade_name=models.CharField(max_length=255)

    def __str__(self):
      return str(self.grade_name)

class Cardgrade(models.Model):
    card_grade_name=models.CharField(max_length=255)

    def __str__(self):
      return str(self.card_grade_name)

class Card_Details(models.Model):
    
    category=models.ForeignKey(Card_Category,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    player_name=models.CharField(max_length=255,blank=True,null=True)
    front_image=models.ImageField(upload_to='front_images',null=True,blank=True)
    upload_time=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    back_thumbnail=models.ImageField(upload_to='back_thumbnails',max_length=255,null=True, blank=True)
    front_thumbnail=models.ImageField(upload_to='front_thumbanils',max_length=255,null=True,blank=True)
    back_image=models.ImageField(upload_to='back_images',null=True,blank=True)
    user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)
    status=models.BooleanField(null=True,blank=True,default=False)
    brand_name=models.CharField(max_length=255,null=True,blank=True)
    card_number=models.CharField(max_length=255,unique=True,null=True,blank=True)
    certification=models.ForeignKey(Certifications,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    certification_number=models.CharField(max_length=255,null=True,blank=True)
    auto_grade=models.ForeignKey(Autograde,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    card_grade=models.ForeignKey(Cardgrade,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    year=models.IntegerField(null=True,blank=True)
    autographed=models.BooleanField(null=True,blank=True)
    is_deleted=models.BooleanField(null=True,blank=False,default=False)

# class CardDetailsNew(models.Model):
#     # front_image=models.ImageField(upload_to='front_images',null=True,blank=True)
#     user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)