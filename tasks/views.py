from django.shortcuts import render , redirect , get_object_or_404 
from tasks.models import UserAccount , UserTasks
from tasks.forms import Register ,Login , TodoInput
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password , check_password
import secrets as secr
# Create your views here.

def index(request):
    if 'email' in request.session:
        
        fetch_user = UserAccount.objects.get(email=request.session['email'])      
        if request.method == 'POST':
            form = TodoInput(request.POST)
            print('Todo data : ',form)
            if form.is_valid():
                task = form.save(commit=False)
                task.account = fetch_user
   
                task.save()
                return redirect('index')
        else:
            getData= UserTasks.objects.filter(account=fetch_user)
               
                 
            form = TodoInput
            return render(request , 'layouts/index.html', {'form': form, 'todo':getData} )
    else:
        return render(request , 'layouts/index.html' )



def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            hashed_pass = make_password(form.cleaned_data['password'])
            user.password = hashed_pass
            user.save()
            return redirect('login')
        else:
            error = 'Invalid Inputs'
            return render(request , 'layouts/register.html' , {'error': error})
    else:
        form = Register
        return render(request , 'layouts/register.html', {'form':form} )




def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            try:
                
                Inputemail = form.cleaned_data['email']
                getData = UserAccount.objects.get(email=Inputemail)
                print('Data retrived :', getData)
                
                if getData.email == Inputemail:
                    if check_password(form.cleaned_data['password'] , getData.password):
                        
                        session_token = str(secr.token_bytes(32))+getData.email
                        request.session['token']= session_token
                        request.session['user'] = getData.name
                        request.session['email'] = getData.email
                        
                        return redirect('index')
                    else:
                        error = 'Password input is wrong'
                        form = Login
                        return render(request , 'layouts/login.html', {'form':form,'error': error } )
                
            except UserAccount.DoesNotExist:
                request.session.flush()
                error = 'User dose not exist or Invalid Inputs'
                form = Login
                return render(request , 'layouts/login.html', {'form':form,'error': error } )
        else:
            error = 'Invalid Inputs'
            return render(request , 'layouts/login.html' , {'error': error})
    else:
        
        form = Login
        return render(request , 'layouts/login.html', {'form':form} )
    
def logout(request):
    request.session.flush()
    return redirect('index')




def delete_task(request , task_id):
    if 'email' in request.session:
        print('EXISTS')
        fetch_task = UserTasks.objects.get(pk=task_id)
        fetch_task.delete() 
        return redirect('index')
    else:
        error = 'The Task cannot be delted by the user'
        return render(request , 'layouts/index.html' , {'error': error}) 
        
   
   
   
def complete_task(request , task_id):
    if 'email' in request.session:
        print('EXISTS')
        fetch_user = UserAccount.objects.get(email=request.session['email']) 
        fetch_task = UserTasks.objects.get(pk=task_id)
        if fetch_user.email == fetch_task.account.email:
            fetch_task.is_completed = not fetch_task.is_completed
            fetch_task.save() 
            return redirect('index')
    else:
        error = 'The Task cannot be accessed'
        return render(request , 'layouts/index.html' , {'error': error}) 
         
         
         
             
def update_task(request , task_id):
    if request.method == "POST":
        if 'email' in request.session:
            form = TodoInput(request.POST)
            if form.is_valid():
                fetch_user = UserAccount.objects.get(email=request.session['email']) 
                fetch_task = UserTasks.objects.get(pk=task_id)
                if fetch_user.email == fetch_task.account.email:
                    fetch_task.todos = form.cleaned_data['todos']
                    fetch_task.save() 
                    return redirect('index')
        else:
            error = 'The Task cannot be accessed'
            return render(request , 'layouts/index.html' , {'error': error}) 
    else:
        fetch_user = UserAccount.objects.get(email=request.session['email']) 
        fetch_task = UserTasks.objects.get(pk=task_id)
        if fetch_user.email == fetch_task.account.email:
            form = TodoInput(instance=fetch_task)
            
            return render(request , 'layouts/index.html', {"form" : form , 'editing': True})
        return redirect('index')
           