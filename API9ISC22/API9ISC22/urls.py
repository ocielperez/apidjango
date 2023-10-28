from django.contrib import admin
from django.urls import path
from api.views import HomeView, LoginView, Inicio, Registro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),  
    path('', HomeView.as_view(), name='raiz'),  
    path('home/', HomeView.as_view(), name='home'),  
    path('inicio/', Inicio.as_view(), name='inicio'),  
    path('registro/', Registro.as_view(), name='registro'),
    # path('formulario/', Formulario.as_view(), name='formulario'),
    # path('formulario/', vista_formulario, name='formulario'),  # Asegúrate que la vista se llama 'vista_formulario'
    # Puedes agregar más rutas según necesites
]
