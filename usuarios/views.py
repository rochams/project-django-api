from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User

def login(request):
    return render(request, 'contas/login.html')




def logout(request):
    return render(request, 'contas/logout.html')




def cadastro(request):
    # messages.success(request, 'Cadastro realizado com sucesso.')  - teste com mensagens
    if request.method != 'POST':
        return render(request, 'contas/cadastro.html')
    
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    nome_usuario = request.POST.get('nome_usuario')
    senha = request.POST.get('senha')
    senha_2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email \
        or not nome_usuario or not senha or not senha_2:
        messages.error(request, 'Favor, preencha todos os campos.')
        return render(request, 'contas/cadastro.html')

    # validação de e-mail
    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido.')
        return render(request, 'contas/cadastro.html')

    if len(senha) < 6:
        messages.error(request, 'Senha muito curta (Mínimo 6 caracteres).')
        return render(request, 'contas/cadastro.html')
    
    if senha != senha_2:
        messages.error(request, 'Senhas precisam ser iguais.')
        return render(request, 'contas/cadastro.html')

    # verificação de e-mail e nome de usuário já existentes na base de dados.
    if User.objects.filter(username=nome_usuario).exists():
        messages.error(request, 'Usuário já existe')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado.')
        return render(request, 'contas/cadastro.html')

    messages.success(request, 'Cadastro realizado com sucesso.')

    user = User.objects.create_user(first_name=nome, last_name=sobrenome, username=nome_usuario, email=email, password=senha)
    user.save()

    return redirect('login')



def dashboard(request):
    return render(request, 'contas/dashboard.html')

