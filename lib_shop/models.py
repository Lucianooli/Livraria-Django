from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    categorias = models.ManyToManyField(Categoria, related_name='livros')
    capa = models.ImageField(upload_to='lib_shop/capas/')
    sinopse = models.TextField(default='')
    descricao = models.TextField(default='')
    pdf = models.FileField(upload_to='lib_shop/pdf/')
    quantidade_paginas = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titulo
    

class saldo_usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    livro_coins = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f' R$ {self.livro_coins}'.replace('.',',')
    

class Biblioteca_usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Biblioteca')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'livro')  # Garante que um usuário não tenha o mesmo livro mais de uma vez

    def __str__(self):
        return f"Biblioteca de {self.usuario.username} - {self.livro.titulo}"