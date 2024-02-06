from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.exceptions import ValidationError,APIException
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework import generics
from .serializers import *
from .authorization import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
# Create your views here.

## login
class InvalidInformationException(APIException):
    status_code = 400
    default_detail = 'Informations invalides'

class MytokenManager(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
            'message': 'Informations invalides',
            'status':status.HTTP_400_BAD_REQUEST, 
        })
            
        
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'login success',
            'status':status.HTTP_200_OK, 
            'id': user.id,
            'role':user.role,
            'email': user.email,
            'nom': user.name,
            'prenom':user.prenom,
            'adress':user.address,
            'date_naissance':user.date_naissance,
            'phone': user.phone,
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })
    
## register 
##REGISTER 
class RegisterVendorAPI(TokenObtainPairView):
    serializer_classes = {
        'Etudiant': RegisterEtudiantSerializer,
        'Manager': RegisterManagerSerializer
    }

    def get_serializer_class(self):
        role = self.request.data.get('role', False)
        serializer_class = self.serializer_classes.get(role)
        return serializer_class

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        role = request.data.get('role', False)

        if phone and password and role:
            serializer_class = self.get_serializer_class()
            if serializer_class is None:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Invalid role'})

            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            try:
                user = serializer.save()
                user.set_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)

                return Response({
                    'phone': user.phone,
                    'name': user.name,
                    'prenom':user.prenom,
                    'address':user.address,
                    'date_naissance':user.date_naissance,
                    'role': user.role,
                    'image': request.data.get('image'),
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            except:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Bad request'})

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'Message': 'Envoyez le numéro de telephone exist'})
    
## cree un cours
class CoursCreateView(generics.CreateAPIView):
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        # Récupérez l'ID du manager à partir du jeton JWT
        manager_id = self.request.user.id
        # Associez le manager au cours
        serializer.save(manager_id=manager_id)
        
        # Récupérez les informations du manager
        manager = Manager.objects.get(id=manager_id)
        
        # Créez un dictionnaire avec les données du manager que vous souhaitez inclure dans la réponse
        manager_data = {
            "nom": manager.name,
            "prenom": manager.prenom,
            "telephone": manager.phone,
            # Ajoutez d'autres champs du manager ici
        }
        
        # Sérialisez le cours créé avec le serializer CoursSerializer
        cours_data = CoursSerializer(serializer.instance).data
        
        # Composez la réponse en incluant à la fois les données du manager et les données du cours
        response_data = {
            "success": 'Le cours a été créé avec succès',
            "manager": manager_data,
            "cours": cours_data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
#------ get courses -------
class CoursGetView(generics.ListCreateAPIView):
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Récupérez l'ID du manager à partir du jeton JWT
        manager_id = self.request.user.id
        # Récupérez la liste des cours associés au manager
        return Cours.objects.filter(manager__id=manager_id)

    def list(self, request, *args, **kwargs):
        # Obtenez la liste des cours à l'aide de la méthode get_queryset
        queryset = self.get_queryset()
        # Sérialisez les cours avec le serializer CoursSerializer
        serializer = self.get_serializer(queryset, many=True)
        # Composez la réponse en incluant les données sérialisées des cours
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#---------- get all courses ----------------    
class CoursGetAllView(generics.ListCreateAPIView):
    serializer_class = CoursSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # Récupérez tous les documents
        documents = Cours.objects.all()
        serializer = CoursSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
#-------- delete courses by id -------------         
class deleteCourses(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]

    def delete(self,request, cours_id):
        # Code pour supprimer un document par son ID
        
        try:
            course = Cours.objects.get(id=cours_id)
            course.delete()
            return Response({'detail': 'course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Cours.DoesNotExist:
            return Response({'detail': 'course not found'}, status=status.HTTP_404_NOT_FOUND) 
        
#-------- delete courses by id -------------   
class updateDocuments(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]

    def put(self, request, course_id):
        # Code pour mettre à jour un document par son ID
        try:
            course = Cours.objects.get(id=course_id)
            serializer = CoursSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cours.DoesNotExist:
            return Response({'message': 'course not found'}, status=status.HTTP_404_NOT_FOUND)   

#poster un video
class VideoCreateView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer  
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]  

#---------get video by courses -------
class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        # Récupérez l'ID du cours à partir des paramètres de requête
        cours_id = self.kwargs.get('cours_id')  # Assurez-vous que vous avez un chemin dans vos URLs pour inclure le cours_id
        # Récupérez la liste des vidéos associées au cours spécifié
        return Video.objects.filter(cours__id=cours_id)

    def list(self, request, *args, **kwargs):
        # Obtenez la liste des vidéos à l'aide de la méthode get_queryset
        queryset = self.get_queryset()
        # Sérialisez les vidéos avec le serializer VideoSerializer
        serializer = self.get_serializer(queryset, many=True)
        # Composez la réponse en incluant les données sérialisées des vidéos
        # response_data = {
        #     "videos": serializer.data
        # }
        return Response(serializer.data, status=status.HTTP_200_OK)  