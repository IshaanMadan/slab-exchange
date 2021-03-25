from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

class LoginTypes(models.Model):
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

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser,PermissionsMixin):
#    full_name=models.CharField(max_length=255,blank=True)
#    name=models.CharField(max_length=30)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    password=models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    create_date=models.DateTimeField(auto_now_add=True)
    login_type=models.ForeignKey(LoginTypes,on_delete=models.CASCADE,default='1')
    authtoken=models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects=UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'users'


class CardCategories(models.Model):
    name=models.CharField(max_length=255,null=False)

    class Meta:
        db_table = 'card_categories'

class CardBrands(models.Model):
    name=models.CharField(max_length=100,null=False)

    class Meta:
        db_table = 'card_brands'

class CardSets(models.Model):
    card_category_id=models.IntegerField()
    year=models.IntegerField(validators=[MaxLengthValidator(4)])
    card_brand=models.ForeignKey(CardBrands,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=False)

    class Meta:
        db_table = 'card_sets'

class CardPlayers(models.Model):
    first_name=models.CharField(max_length=100,null=False)
    last_name=models.CharField(max_length=100,null=False)

    class Meta:
        db_table = 'card_players'

class CardArtists(models.Model):
    name=models.CharField(max_length=100,null=False)
    name2=models.CharField(max_length=100,null=True)
    website=models.CharField(max_length=100)
    instagram=models.CharField(max_length=100)

    class Meta:
        db_table = 'card_artists'


class Certifications(models.Model):
    certificate_name=models.CharField(max_length=255)

    def __str__(self):
      return str(self.certificate_name)

class CardTeams(models.Model):

    full_name=models.CharField(max_length=100,null=False)
    short_name=models.CharField(max_length=100,null=False)
    abbreviation=models.CharField(max_length=100,null=False)

    class Meta:
        db_table = 'card_teams'

class Cards(models.Model):
    
    release_date=models.DateField(null=True,blank=True)
    card_category=models.ForeignKey(CardCategories,on_delete=models.CASCADE)
    card_brand=models.ForeignKey(CardBrands,on_delete=models.CASCADE)
    card_set=models.ForeignKey(CardSets,on_delete=models.CASCADE)
    number=models.IntegerField()
    year=models.IntegerField(null=True)
    card_player=models.ForeignKey(CardPlayers,on_delete=models.CASCADE)
    card_artist=models.ForeignKey(CardArtists,on_delete=models.CASCADE)
    card_team=models.ForeignKey(CardTeams,on_delete=models.CASCADE)

    class Meta:
        db_table = 'cards'


class CardVersions(models.Model):
  
    release_date=models.DateField()
    card=models.ForeignKey(Cards,on_delete=models.CASCADE,null=False)
    name=models.CharField(max_length=100,null=False)
    print_run=models.IntegerField()
    is_companion=models.BooleanField(default=False)
    is_customized=models.BooleanField(default=False)
    is_artist_auto=models.BooleanField(default=False)
    is_player_auto=models.BooleanField(default=False)

    class Meta:
        db_table = 'card_versions'

class CardKeywords(models.Model):
    
    card=models.ForeignKey(Cards,on_delete=models.CASCADE)
    card_version=models.ForeignKey(CardVersions,on_delete=models.CASCADE)
    keyword_string=models.CharField(max_length=255)

    class Meta:
        db_table = 'card_keywords'

class CardGradingCompanies(models.Model):
    
    abbreviation=models.CharField(max_length=255)
    name=models.CharField(max_length=255)

    class Meta:
        db_table = 'card_grading_companies'

class AutoGrades(models.Model):
    value=models.CharField(max_length=255)

    class Meta:
        db_table = 'auto_grades'

class CardGrades(models.Model):
    value=models.CharField(max_length=255)

    class Meta:
        db_table = 'card_grades'


class UserCards(models.Model):

    
    user=models.ForeignKey(Users,on_delete=models.CASCADE,null=True,blank=True)
    card=models.ForeignKey(Cards,on_delete=models.CASCADE)
    card_version=models.ForeignKey(CardVersions,on_delete=models.CASCADE)
    grading_company=models.ForeignKey(CardGradingCompanies,on_delete=models.CASCADE)
    card_grade=models.ForeignKey(CardGrades,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    is_auto=models.BooleanField(null=True,default=False)
    auto_grade=models.ForeignKey(AutoGrades,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    certification_number=models.IntegerField(null=True,blank=True)
    front_image=models.ImageField(upload_to='front_images',max_length=255,null=True,blank=True)
    back_image=models.ImageField(upload_to='back_images',max_length=255,null=True,blank=True)
    front_thumbnail=models.ImageField(upload_to='front_thumbanils',max_length=255,null=True,blank=True)
    back_thumbnail=models.ImageField(upload_to='back_thumbnails',max_length=255,null=True, blank=True)
    created_date=models.DateField(auto_now_add=True,null=True,blank=True)

    class Meta:
        db_table = 'user_cards'
    
    # category=models.ForeignKey(Card_Category,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    # player_name=models.CharField(max_length=255,blank=True,null=True)
    # status=models.BooleanField(null=True,blank=True,default=False)
    # brand_name=models.CharField(max_length=255,null=True,blank=True)
    # card_number=models.CharField(max_length=255,unique=True,null=True,blank=True)
    # certification=models.ForeignKey(Certifications,on_delete=models.CASCADE,max_length=255,null=True,blank=True)
    # certification_number=models.CharField(max_length=255,null=True,blank=True)
    # year=models.IntegerField(null=True,blank=True)
    # autographed=models.BooleanField(null=True,blank=True)
    

# class CardDetailsNew(models.Model):
#     # front_image=models.ImageField(upload_to='front_images',null=True,blank=True)
#     user=models.ForeignKey(User_Details,on_delete=models.CASCADE,null=True,blank=True)