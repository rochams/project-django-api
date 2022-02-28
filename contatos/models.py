
from django.utils import timezone
from django.db import models


class Categoria(models.Model):
    # para criar a chave estrangeira, instanciamos outra classe com ela.
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    # o argumento on_delete indica o que fazer com os dados quando determinada categoria for deletada, nesse caso a ação escolhida foi não fazer nada.
    mostrar = models.BooleanField(default=True)

    def __str__(self):
        return self.nome



