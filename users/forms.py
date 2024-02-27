from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
#Gera o formulário de criação de conta

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        

