from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Livro, Categoria, saldo_usuario, Biblioteca_usuario
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm  # Importe a sua classe customizada
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def home_page(request):
    livros = Livro.objects.all()
    categoria = Categoria.objects.all()
    try:
        ficcao_categoria = Categoria.objects.get(id=4)
        ficcaos = ficcao_categoria.livros.all()  # Filtra os livros pela categoria
    except Categoria.DoesNotExist:
        ficcaos = []
    try:
        romance_categoria = Categoria.objects.get(id=3)
        romance = romance_categoria.livros.all()
    except Categoria.DoesNotExist:
        romance = []

    return render(request, 'lib_shop/home_page.html', {'livros': livros, 'ficcaos': ficcaos, 'romance': romance, 'categoria': categoria})

class LogoutGetView(View):
    def get(self, request):
        logout(request)
        return redirect('home')



@login_required
def Livro_pagina(request, livro_id):
    categoria = Categoria.objects.all()
    livro = get_object_or_404(Livro, id=livro_id)
    saldo = None
    ja_possui_livro = False  # Inicializa a variável como False

    if request.user.is_authenticated:
        # Garante que o saldo do usuário exista
        saldo, created = saldo_usuario.objects.get_or_create(usuario=request.user, defaults={'livro_coins': 0})

        # Verifica se o livro já está na biblioteca do usuário
        ja_possui_livro = Biblioteca_usuario.objects.filter(usuario=request.user, livro=livro).exists()

        if not ja_possui_livro:
            # Verifica se o saldo é suficiente para a compra
            if livro.preco <= saldo.livro_coins:
                # Realiza a compra e adiciona o livro à biblioteca
                Biblioteca_usuario.objects.create(usuario=request.user, livro=livro)
                # Atualiza o saldo do usuário
                saldo.livro_coins -= livro.preco
                saldo.save()
                messages.success(request, "Você comprou o livro com sucesso!")
            else:
                messages.error(request, "Saldo insuficiente.")
    else:
        messages.error(request, "Você precisa estar logado para realizar compras.")

    return render(request, 'lib_shop/books.html', {
        'livro': livro,
        'categoria': categoria,
        'saldo': saldo,
        'ja_possui_livro': ja_possui_livro,  # Passa a condição para o template
    })


    

def Categoria_pagina(request, categoria_id):
    categoria = Categoria.objects.all()
    livros = []
    try:
        categoria_pag = get_object_or_404(Categoria, id=categoria_id)
        livros = categoria_pag.livros.all()
    except:
        categoria_pag = None
    return render(request, 'lib_shop/pag_categoria.html',{'categoria_pag':categoria_pag, 'categoria':categoria , 'livros': livros})



def pesquisar(request):
    query = request.GET.get('q')
    if query:
        livros = Livro.objects.filter(titulo__icontains=query) | Livro.objects.filter(autor__icontains=query)
    else:
        livros = Livro.objects.none()  # Se não houver query, não retorna nenhum livro
    
    return render(request, 'lib_shop/pesquisa_resultados.html', {'livros': livros, 'query': query})



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirecione para a página de login ou outra página
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserRegistrationForm()
    return render(request, 'lib_shop/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Você foi logado com sucesso.')

            # Redireciona para a página que o usuário tentou acessar, se houver
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')  # Ou a página padrão após o login
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'lib_shop/login.html', {'form': form})

@login_required
def biblioteca(request):
    if request.user.is_authenticated:
        livros = Biblioteca_usuario.objects.filter(usuario=request.user).select_related('livro')
    else:
        livros = []  # ou redirecione para a página de login, se preferir

    return render(request, 'lib_shop/biblioteca.html', {
        'livros': livros,
    })


@login_required
def verificar_biblioteca(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    possui = Biblioteca_usuario.objects.filter(usuario=request.user, livro=livro).exists()
    return JsonResponse({'possui': possui})


def Banco_coins(request):
    return render(request,'lib_shop/banco.html')