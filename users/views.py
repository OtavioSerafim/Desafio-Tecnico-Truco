from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

#Gera a página de registro e os formulários necessários além da lógica presente no processo de registro
def register(request):
    
    #Cria a condicional para caso um formulário seja enviado, confere se ele é válido
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #Se ele for válido, salva o formulário informa o usuário, e redireciona para o login
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'A conta foi criada com sucesso!')
            return redirect('Site-inicio')
        
    #Do contrário mostra ao usuário a página de registro.        
    else:
        form = UserRegisterForm()
        
    return render(request, 'users/register.html', {'form': form})
