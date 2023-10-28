from django.contrib import admin
from .models import UserIbtikar,Etudiant,Manager,Cours,Video,Transaction
# Register your models here.

admin.site.site_header = "IBTIKAR"

class UserAdminConfig(admin.ModelAdmin):
    model = UserIbtikar
    search_fields = ('email', 'name', 'phone','prenom',)
    list_filter = ('email', 'name', 'phone', 'is_active', 'is_staff')
    ordering = ('name',)  # Update the ordering field here
    list_display = ('phone','email', 'name', 'prenom','is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'prenom','phone','role',)}),
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

admin.site.register(UserIbtikar, UserAdminConfig)
admin.site.register(Etudiant, UserManager)
admin.site.register(Manager, UserManager)
admin.site.register(Cours)
admin.site.register(Video)
admin.site.register(Transaction)