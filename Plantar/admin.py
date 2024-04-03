from django.contrib import admin
from django.contrib.auth.models import Group,User
from  django.db.models import Count
from . import models




class ProfileInline(admin.StackedInline):
    model = models.Profile
    

class customUser(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]
    
    
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User,customUser)



@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user']

@admin.register(models.Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['id','user_name','body','create_at']
    list_per_page = 10
    search_fields = ['body']
    
    
    def user_name(self,plant):
        return plant.user.username
    

@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name','creator']
    list_per_page = 10
    search_fields = ['name']
    
    

@admin.register(models.ChannelPost)
class ChannelPostAdmin(admin.ModelAdmin):
    list_display = ['channel','author','body','create_at']
    list_per_page = 10
    search_fields = ['author']