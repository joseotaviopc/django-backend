from django.db import models

# Create your models here.
faixa_choices = (
        ('B', 'Branca'),
        ('A', 'Azul'),
        ('R', 'Roxa'),
        ('M', 'Marrom'),
        ('P', 'Preta')
    )

class AlunosModel(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    faixa = models.CharField(max_length=1, choices=faixa_choices, default='B')
    data_nascimento = models.DateField(null=True, blank=True)

    def data_nascimento_formatada(self):
        date_value = self.data_nascimento
        return date_value.strftime('%d/%m/%Y')

    def __str__(self):
        return self.nome

class AulasConcluidas(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(AlunosModel, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    faixa_atual = models.CharField(max_length=1, choices=faixa_choices)

    def __str__(self):
        return self.aluno.nome
