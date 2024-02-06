from django.contrib import admin
from .models import UserIbtikar,Etudiant,Manager,Cours,Video,Transaction
# Register your models here.

admin.site.site_header = "IBTIKAR"

class UserAdminConfig(admin.ModelAdmin):
    model = UserIbtikar
    search_fields = ('email', 'name', 'phone','prenom','password')
    list_filter = ('email', 'name', 'phone', 'is_active', 'is_staff')
    ordering = ('name',)  # Update the ordering field here
    list_display = ('phone','email', 'name', 'prenom','is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'prenom','phone','role','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','prenom','phone', 'is_active', 'is_staff', 'is_blocked')
            }
         ),
    )

class UserManager(admin.ModelAdmin):
    model = UserIbtikar
    search_fields = ('email', 'name', 'phone','prenom',)
    list_filter = ('email', 'name', 'phone', 'is_active', 'is_staff')
    ordering = ('name',)  # Update the ordering field here
    list_display = ('phone','prenom','email', 'name', 'is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone','image','role','prenom')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'prenom','phone', 'is_active', 'is_staff', 'is_blocked')
            }
         ),
    )

class CoursConf(admin.ModelAdmin):
    model = Cours
    search_fields = ('titre','description','image','prix','manager')
    list_filter = ('titre','description','image','prix','manager')
    ordering = ('titre',)  # Update the ordering field here
    list_display = ('titre','description','image','prix','manager')
    fieldsets = (
        (None, {'fields': ('titre','description','image','prix','manager')}),
        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('titre','description','image','prix','manager')
            }
         ),
    )  

class VideoConf(admin.ModelAdmin):
    model = Video
    search_fields = ('titre','fichier_video','date_upload','cours')
    list_filter = ('titre','fichier_video','date_upload','cours')
    ordering = ('titre',)  # Update the ordering field here
    list_display = ('titre','fichier_video','date_upload','cours')
    fieldsets = (
        (None, {'fields': ('titre','fichier_video','cours')}),
        
    )  
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('titre','fichier_video','cours')
            }
         ),
    )      

admin.site.register(UserIbtikar, UserAdminConfig)
admin.site.register(Etudiant, UserManager)
admin.site.register(Manager, UserManager)
admin.site.register(Cours,CoursConf)
admin.site.register(Video,VideoConf)
admin.site.register(Transaction)