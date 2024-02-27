from django.contrib import admin
from django.urls import path
from Site import views as site_views
from Site import views_ordem as site_views_ordem
from users import views as user_views
from django.contrib.auth import views as auth_views

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
    
]
