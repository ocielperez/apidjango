from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import CustomUser, Formulario
from .models import Formulario

class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginView(View):
    template_name = 'index.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        email = request.POST.get('username')  # Cambiado a email para claridad
        password = request.POST.get('password')
        
        # Intentar autenticar al usuario utilizando el email
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('inicio')  # O donde quieras redirigir al usuario después del login
        else:
            messages.error(request, 'Credenciales inválidas. Por favor intenta de nuevo.')
            return render(request, self.template_name)


class Inicio(View):
    def get(self, request):
        grafica_data = grafica(request)
        tuvista_data = consulta1(request)
        tuvista_data2 = consulta2(request)
        tuvista_data3 = consulta3(request)
        
        # Combina los contextos de ambas vistas en un solo diccionario
        context = {**grafica_data, **tuvista_data, **tuvista_data2, **tuvista_data3}
        return render(request, 'inicio.html', context)

def grafica(request):
    registros = Formulario.objects.all()
    return {'registros': registros}

def consulta1(request):
    # Realiza una consulta que cuente las filas con 'SI' en la columna pregunta1
    count = Formulario.objects.filter(respuesta1="10").count()
    return {'count_10': count}

def consulta2(request):
    # Realiza una consulta que cuente las filas con 'NO' en la columna pregunta1
    count2 = Formulario.objects.filter(respuesta1="9").count()
    return {'count_9': count2}

def consulta3(request):
    # Realiza una consulta que cuente las filas con 'NO' en la columna pregunta1
    count3 = Formulario.objects.filter(respuesta1="8").count()
    return {'count_8': count3}





class Registro(View):
    template_name = 'registro.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')

        try:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
                return render(request, self.template_name)

            user = CustomUser.objects.create_user(
                email=email,
                password=contraseña,
                first_name=nombre,
                last_name=apellidos,
                birth_year=fecha_nacimiento.split('-')[0]
            )

            messages.success(request, "Te has registrado exitosamente. Por favor inicia sesión.")
            return redirect('login')  # Redirigir a la página de inicio de sesión después de un registro exitoso

        except IntegrityError:
            messages.error(request, 'Hubo un error al registrar el usuario.')
            return render(request, self.template_name)





#sqlite
# def vista_formulario(request):
#     if request.method == 'POST':
#         nombre = request.POST.get('nombre')
#         edad = request.POST.get('edad')
#         respuesta1 = request.POST.get('respuesta1')
#         respuesta2 = request.POST.get('respuesta2')
#         respuesta3 = request.POST.get('respuesta3')

#         # Verificar si algún campo está vacío
#         if not (nombre and edad and respuesta1 and respuesta2 and respuesta3):
#             messages.error(request, 'Todos los campos son requeridos.')
#             return render(request, 'formulario.html')
        
#         # Asegurarse de que la edad sea un número entero
#         try:
#             edad = int(edad)
#         except ValueError:
#             messages.error(request, 'La edad debe ser un número.')
#             return render(request, 'formulario.html')
        
#         # Asegurarse de que las respuestas sean números enteros
#         try:
#             respuesta1 = int(respuesta1)
#             respuesta2 = int(respuesta2)
#             respuesta3 = int(respuesta3)
#         except ValueError:
#             messages.error(request, 'Las respuestas deben ser números.')
#             return render(request, 'formulario.html')

#         # Intentar guardar los datos en la base de datos
#         try:
#             formulario = Formulario(
#                 nombre=nombre, 
#                 edad=edad, 
#                 respuesta1=respuesta1, 
#                 respuesta2=respuesta2, 
#                 respuesta3=respuesta3
#             )
#             formulario.save()
#             messages.success(request, 'Formulario guardado exitosamente.')
#             return redirect('resultado_exitoso')  
#         except Exception as e:
#             messages.error(request, f"Error al guardar el formulario: {e}")
#             return render(request, 'formulario.html')
            
#     return render(request, 'formulario.html')
