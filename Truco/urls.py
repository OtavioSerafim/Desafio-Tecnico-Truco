from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Site import views as site_views, views_ordem as site_views_ordem
from jogo import views as jogo_views, views_truco as jogo_views_truco, logica_jogo as logica_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', site_views.inicio, name= 'Site-inicio'),
    
    path('home/', site_views.home, name='Site-Home'),
    
    path('regras/', site_views.regras, name='Site-Regras'),
    
    path('ordem/', site_views_ordem.ordem, name='Site-Ordem'),
    
    path('ordem/2/', site_views_ordem.ordem_2, name='Site-Ordem-2'),
    
    path('register/', user_views.register, name= 'register'),
    
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='Site-inicio'), name = 'logout'),
    
    path('leaderboards/', site_views.leaderboards, name='Site-leaderboards'),
    
    path('confirmacao/', site_views.confirmacao, name='Site-confirmacao'),
    
    path('jogo/', jogo_views.inicio_jogo, name= 'Jogo-inicio'),
    
    path('jogo/resultado/', jogo_views.resultado, name= 'Jogo-Resultado'),
    
    path('jogo/truco/', jogo_views_truco.jogo, name='Jogo-Truco'),
    
    path('jogo/move_card/', logica_views.move_card, name='Jogo-movecard'),
    
    path('jogo/pedido_truco/', logica_views.pedido_truco, name='Jogo-pedir-truco'),
    
]
