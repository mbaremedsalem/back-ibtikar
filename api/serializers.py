from .models import *
from rest_framework import serializers 
from django.contrib.auth import authenticate

class UserManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Manager
        fields= ('phone','name')

class UserEtutiantSerializer(serializers.ModelSerializer):
    class Meta:
        model= Etudiant
        fields= ('phone','name')

## serializer login

class MyTokenObtainPairSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_blocked:
            user.number_attempt=0
            user.save()
            return user
        
        elif user and user.is_active and user.is_blocked:
            # return Response('message')
            # return Response(serializers.errors)
            
            raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        
        try:
            obj= Manager.objects.get(phone=data['phone'])
            if obj.number_attempt<3:
                obj.number_attempt +=1
                obj.save()
                raise serializers.ValidationError({'message':'Informations invalides.'})
            else:
                obj.number_attempt +=1
                obj.is_blocked=True
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        except:
            raise serializers.ValidationError({'message':'Informations invalides.'})   
      
## serialize register 

## register manager 
class RegisterManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ('id', 'phone', 'name','prenom','address','date_naissance','email','password','role','image')
        extra_kwargs = {
            'password': {'write_only': True}
        }

## register Etudiant 
class RegisterEtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ('id', 'phone','name','prenom','address','date_naissance','email', 'password','role','image')
        extra_kwargs = {
            'password': {'write_only': True}
        }


## cours serializer
class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = ('titre', 'description','image','prix')

## video serialiser
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('titre','fichier_video','cours')        
        