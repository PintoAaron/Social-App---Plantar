from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from.models import Profile,Plant,Channel,ChannelPost
from .forms import PlantForm,RegisterForm,ChannelPostForm


def hello(request):
    return HttpResponse('HELLO GUYS')


def home(request):
    if request.user.is_authenticated:
        form = PlantForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                plant = form.save(commit = False)
                plant.user = request.user
                plant.save()
                messages.success(request,"Your Plant has being posted")
                return redirect('home')
                    
        plants= Plant.objects.all().order_by('-create_at')
        return render(request,'home.html',{'plants':plants,"form":form})
    else:
        plants= Plant.objects.all().order_by('-create_at')
        return render(request,'home.html',{'plants':plants})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        context = {'profiles':profiles}
        return render(request,'profile_list.html',context)
    else:
        messages.success(request,"Please log in to view this Page")
        return redirect('home')
    
def profile(request,id):
    if request.user.is_authenticated:
        profile = Profile.objects.get(pk = id)
        plants = Plant.objects.filter(user_id = id)
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "follow":
                current_user_profile.follows.add(profile)
            elif action == "unfollow":
                current_user_profile.follows.remove(profile)
            current_user_profile.save()
        context = {'profile':profile,'plants':plants}
        return render(request,'profile.html',context)
    else:
        messages.success(request,"Please log in to view this Page")
        return redirect('home')
    
        



def login_user(request):
    if request.method == "POST":
        user_username = request.POST['username']
        user_password = request.POST['password']
        user  = authenticate(request,username = user_username,password= user_password)
        if user is not None:
            login(request,user)
            messages.success(request,("You Have Successfully Logged In"))
            return redirect('home')
        else:
            messages.success(request,"No account with these credentials found")
            return redirect('login')
    return render(request,'login.html',{})
    

def logout_user(request):
    logout(request)
    messages.success(request,"Logged Out!!!")
    return redirect('home')


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You Have Successfully registered "))
            return redirect('home')
    return render(request,'register.html',{'form':form})


def channel_list(request):
    channels = Channel.objects.all().order_by('name')
    context = {'channels':channels}
    return render(request,'channel_list.html',context)




def channel(request,id):
    if request.user.is_authenticated:
        current_channel = Channel.objects.get(pk = id)
        form = ChannelPostForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                channel_post = form.save(commit = False)
                channel_post.author = request.user
                channel_post.channel = current_channel
                channel_post.save()
                messages.success(request,"Your have successfully posted to channel")
                return redirect('channel',id)
        
        channel_posts = ChannelPost.objects.filter(channel_id = id).order_by('-create_at')
        context = {'channel':current_channel,'channel_posts':channel_posts,'form':form}
        return render(request,'channel.html',context)
    