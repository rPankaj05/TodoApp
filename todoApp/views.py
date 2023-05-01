from django.shortcuts import render , redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
# Create your views here.
from todoApp.forms import TODOForm,TODO
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user=request.user
        form=TODOForm()
        todos=TODO.objects.filter(user =user).order_by('priority')
        context={
            'form':form,
            'todos':todos,
         }
        return render(request,'index.html',context=context) 
    

def login(request): 
    if request.method=='GET':
        form=AuthenticationForm()
        context={
            'form':form
        }
        return render(request,'login.html',context=context)
    else:
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                loginUser(request,user)
                return redirect('home')

        else:
            context={
            'form':form
              }
            return render(request,'login.html',context=context)
            

         


def signup(request): 
    if request.method=='GET':
        form=UserCreationForm()
        context={
            'form':form
            }
        return render(request,'signup.html',context=context)
         
    
    else:
        form=UserCreationForm(request.POST)
        context={
            'form':form
            }
        
        if form.is_valid():
            user=form.save()
            return redirect('login')
        
        else:
            return render(request,'signup.html',context=context)
        


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        form=TODOForm(request.POST)
        if form.is_valid():
            todo=form.save(commit=False)
            todo.user=user
            todo.save()
            return redirect('home')
        else:
            context={
               'form':form
                }
            return render(request,'index.html',context=context)


@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')


def delete_todo(request,id):
    TODO.objects.get(pk=id).delete()
    return redirect('home')


def change_status(request,id,status):
    todo=TODO.objects.get(pk=id)
    todo.status=status
    todo.save()
    return redirect('home')