from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from blog.models import Blogcomments
from .forms import UserRegisterForm
from blog.templatetags import extras
 #Create your views here.


def home(request, ):
    comments = Blogcomments.objects.filter(parent = None)
    replies = Blogcomments.objects.all().exclude(parent = None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
           replyDict[reply.parent.sno].append(reply)

    context = {'comments': comments, 'user': request.user,'replyDict': replyDict}
    return render(request, 'home.html', context)





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        
        user = authenticate( username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, 'Succesfully Logged in')
            return redirect('productview')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('home')
        
    else:
        return HttpResponse('error 404 - not found')


def handleLogout(request):
    logout(request)
    messages.success(request, 'Succesfully Logged out')
    return redirect('home')
        
def postcomment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user    
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = Blogcomments(comment = comment, user = user)
            comment.save()
            messages.success(request, 'Your Comment has been posted Succesfully')
        else:
            parent = Blogcomments.objects.get(sno = parentSno)
            comment = Blogcomments(comment = comment, user = user, parent= parent)
            comment.save()
            messages.success(request, 'Your Reply has been posted Succesfully')
        return redirect('home')



