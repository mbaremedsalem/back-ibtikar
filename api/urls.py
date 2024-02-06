from django.urls import path
from .views import *
urlpatterns = [
    ####----------login---------------#####
    path('login/', MytokenManager.as_view(), name='token_obtain_pairManager'),
    ####---------register-------------#####
    path('register/', RegisterVendorAPI.as_view(), name='user-registerVendor'),
    ##-----------crete cours---------------#####
    path('cours/create/', CoursCreateView.as_view(), name='cours-create'),
    ##-----------get cours---------------#####
    path('cours/get-course-by-manager/', CoursGetView.as_view(), name='cours-get-id'),
    ####---------get all courses ---
    path('cours/get-all-courses/', CoursGetAllView.as_view(), name='cours-get-all'),
    ####--------delete course by id  --------
    path('cours/delete/<int:cours_id>', deleteCourses.as_view(), name='cours-delet-id'),
    ####--------update course by id  --------
    path('cours/update/<int:cours_id>', updateDocuments.as_view(), name='cours-update-id'),
    ####--------video---------
    path('videos/create/', VideoCreateView.as_view(), name='video-create'),
    ####--------get video by courses ---------
    path('cours/<int:cours_id>/videos/', VideoListView.as_view(), name='video-get-in-courses'),

    
    
]
