from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager 
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

Role=(
    ('Manager', 'Manager'),
    ('Etudiant', 'Etudiant'),
)  

class UserIbtikar(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=50,blank=True)
    prenom = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=16,unique=True)
    email = models.EmailField(max_length=50,blank=True)
    date_naissance = models.DateTimeField(null=True)
    address = models.CharField(max_length=200,)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role= models.CharField(max_length=30, choices=Role, default='Manager')
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    def __str__(self): 
        return self.name 
    
def image_uoload_profile(instance,filname):
    imagename,extention =  filname.split(".")
    return "user/%s.%s"%(instance.id,extention)    

class Etudiant(UserIbtikar):
    image=models.ImageField(upload_to=image_uoload_profile ,null=True)
    def __str__(self): 
        return self.phone 
        
#--------manager -----------
class Manager(UserIbtikar):
    image=models.ImageField(upload_to=image_uoload_profile ,null=True)   

    def __str__(self): 
        return self.phone     
def image_uoload_course(instance,filname):
    imagename,extention =  filname.split(".")
    return "video-image/%s.%s"%(instance.id,extention)  
    
class Cours(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to=image_uoload_course ,null=True) 
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titre
    

class Video(models.Model):
    titre = models.CharField(max_length=100)
    fichier_video = models.FileField(upload_to='videos/')
    date_upload = models.DateTimeField(auto_now_add=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='videos')
    def __str__(self):
        return self.titre   
    
class Transaction(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    numTransaction = models.CharField(max_length=200,blank=True)
    amount = models.FloatField()
    def __str__(self):
        return f"Transaction de {self.etudiant.nom} pour {self.cours.titre}"
