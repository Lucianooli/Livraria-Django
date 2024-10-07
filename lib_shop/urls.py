from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home_page,name='home'),
    path('livros/<int:livro_id>/',views.Livro_pagina,name='books'),
    path('categorias/<int:categoria_id>/', views.Categoria_pagina,name='categorias_pag'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.LogoutGetView.as_view(),name='logout'),
    path('biblioteca/', views.biblioteca, name='biblioteca_usuario'),
    path('verificar_biblioteca/<int:livro_id>/', views.verificar_biblioteca, name='verificar_biblioteca'),
    path('banco/', views.Banco_coins, name='banco')



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)