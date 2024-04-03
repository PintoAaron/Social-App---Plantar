from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Channel(models.Model):
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField()
    creator = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='created_channels')
    chaneel_subscribers = models.ManyToManyField(User,related_name='subscribed_channels',symmetrical=False,blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class ChannelPost(models.Model):
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return (f"{self.channel.name }  " 
                f"{self.author.username}  "
                f"{self.create_at:%Y-%m-%d %H:%M:%S }  " 
                f"{self.body}")
    
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)
    date_modefied = models.DateTimeField(User,auto_now= True)
    subscribed_channels = models.ManyToManyField(Channel,related_name='subscribers',symmetrical=False,blank=True) 
    
    def __str__(self) -> str:
        return self.user.username
    
    
@receiver(post_save, sender=User)    
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
        
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

        
class Plant(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='plants')
    body = models.CharField(max_length=200,null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return (f"{self.user }  " 
                f"{self.create_at:%Y-%m-%d %H:%M:}  " 
                f"{self.body}")
    
        
        
    
