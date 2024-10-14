from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse
import random

# Create your models here.
from django.contrib.auth.models import User

class Curso(models.Model):
    usuario = models.ManyToManyField(User, related_name='cursos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    codigo = models.CharField(max_length=10, unique=True)
    duracao = models.IntegerField(help_text="Duração em horas")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    professor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, related_name='cursos')

    def __str__(self):
        return self.nome


class Professor(models.Model):
    usuario = models.ManyToManyField(User, related_name='professores')
    nome = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True)
    data_nascimento = models.DateField()
    data_matricula = models.DateField()
    matricula = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nome


class Estudante(models.Model):
    usuario = models.ManyToManyField(User, related_name='estudantes')
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=10, unique=True)
    data_nascimento = models.DateField()
    data_matricula = models.DateField()
    telefone = models.CharField(max_length=18, blank=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True)
    cursos = models.ManyToManyField(Curso, related_name='estudantes')

    def __str__(self):
        return self.nome
    
    def get_edit_url(self):
        return reverse('edit-student', args=[str(self.id)])

    def gerar_matricula(self):
        while True:
            matricula = f'ES{random.randint(1000000, 9999999)}'
            if not Estudante.objects.filter(user=self.user,matricula=matricula).exists():
                return matricula
            
    def save(self, *args, **kwargs):
        if not self.matricula:  # Gera a matrícula apenas se não existir
            self.matricula = self.gerar_matricula()
        super().save(*args, **kwargs)