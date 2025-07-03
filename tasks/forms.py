from django import forms
from tasks.models import UserAccount , UserTasks

class Register(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = UserAccount
        fields = [
            'name','email','password'
        ]
class Login(forms.Form):
    
    password = forms.CharField(widget=forms.PasswordInput)  
    email = forms.EmailField()
    class Meta:
        model = UserAccount
        fields = [
            'email','password'
        ]   


class TodoInput(forms.ModelForm):
    class Meta:
        model = UserTasks
        fields = [
        "todos"
        ]