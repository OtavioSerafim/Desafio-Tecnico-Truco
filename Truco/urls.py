from django.contrib import admin
from django.urls import path
from Site import views as site_views
from Site import views_ordem as site_views_ordem


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', site_views.inicio, name= 'Site-inicio'),
    
    path('home/', site_views.home, name='Site-Home'),
    
    path('regras/', site_views.regras, name='Site-Regras'),
    
    path('ordem/', site_views_ordem.ordem, name='Site-Ordem'),
    
    path('ordem/2/', site_views_ordem.ordem_2, name='Site-Ordem-2')
    
]
