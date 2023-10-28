from django.urls import path
from .views import *
urlpatterns = [
    ####----------login---------------#####
    path('login/', MytokenManager.as_view(), name='token_obtain_pairManager'),
    ####---------register-------------#####
    path('register/', RegisterVendorAPI.as_view(), name='user-registerVendor'),
    ##-----------cours---------------#####
    path('cours/create/', CoursCreateView.as_view(), name='cours-create'),
    ####--------video---------
    path('videos/create/', VideoCreateView.as_view(), name='video-create'),
    
]
