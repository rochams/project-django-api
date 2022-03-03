
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato

def login(request):

    if request.method != 'POST':
        return render(request, 'contas/login.html')

    usuario = request.POST.get('usuario')   # pegando informações de login inseridas pelo usuário
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)  # autenticação do usuário
    # se não houver a autenticação, o resultado coletado em 'user' é 'None'

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'contas/login.html')
    
    else:
        auth.login(request, user)
        messages.success(request, f'Olá, {user.first_name}. Esta é a área administrativa do sistema.')
        return redirect('dashboard')
        


def logout(request):
    auth.logout(request)
    return render(request, 'contas/login.html')



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


@login_required(redirect_field_name='login')
def dashboard(request):
    # caso não seja enviado nenhum campo, a página se mantém.
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'contas/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)
    
    if not form.is_valid():
        # retornando erro em caso de haver algum ou alguns campos incorretamente preenchidos.
        messages.error(request, 'Preencha corretamente todos os campos.')
        form = FormContato(request.POST)
        return render(request, 'contas/dashboard.html', {'form': form})

    email = validate_email(request.POST.get('email'))
    if email == 'None':
        messages.error(request, 'E-mail inválido.')
        return render(request, 'contas/dashboard.html')
        
    form.save()
    messages.success(request, 'Contato salvo com sucesso.')
    return redirect('dashboard')
