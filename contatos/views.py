from django.shortcuts import get_object_or_404, render, redirect
from .models import Contato
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    """ função para a página inicial"""
    dados = Contato.objects.order_by('nome').filter(
        mostrar=True
    )                                           # ordenando por nomes em ordem crescente e exibindo somente itens com 'mostrar' habilitados.
    paginator = Paginator(dados, 10)            # limitando a exibição de 10 contatos por página.
    pagina = request.GET.get('pag')              # .GET.get é usado em dicionários. Ou seja, está obtendo o valor da variável aqui chamada de 'pg'.
    contatos = paginator.get_page(pagina)

    return render(request, 'contatos/index.html', {'contatos': contatos })


def ver_contato(request, contato_id):
    """ função para visualizar contatos separadamente"""
    contato = get_object_or_404(Contato, id=contato_id)
    return render(request, 'contatos/contato.html', {'contato': contato})


def busca(request):
    """ função que busca contatos"""
    termo = request.GET.get('termo')                        # jogando termo pesquisado para dentro da variável 'termo'.

    if not termo or termo is None:
        messages.add_message(request, messages.ERROR, 'Por favor, digite algo.')
        return redirect('index')
        
    campos = Concat('nome', Value(' '), 'sobrenome')

    dados = Contato.objects.annotate(
        nome_completo = campos,
    ).filter(
        nome_completo__icontains=termo,                     # a barra 'pipe' tem significado de 'OU' no método Q.
        mostrar=True
    )

    paginator = Paginator(dados, 10)            
    pagina = request.GET.get('pag')             
    contatos = paginator.get_page(pagina)

    return render(request, 'contatos/busca.html', {'contatos': contatos})

