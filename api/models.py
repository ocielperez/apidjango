from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Asegúrate de que la clase Formulario esté definida en este archivo si la vas a utilizar

class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para crear usuarios y superusuarios.
    """
    
    def create_user(self, email, first_name, last_name, birth_year, password=None, **extra_fields):
        """
        Crea y devuelve un usuario regular con un email y contraseña.
        """
        
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, birth_year=birth_year, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, birth_year, password=None, **extra_fields):
        """
        Crea y devuelve un superusuario con un email y contraseña.
        """
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, birth_year, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo personalizado de usuario que soporta el uso de un email 
    en lugar de un username.
    """
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_year']
    
    # Agregar related_name para evitar conflictos con los campos groups y user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.email

class Formulario(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    respuesta1 = models.IntegerField()
    respuesta2 = models.IntegerField()
    respuesta3 = models.IntegerField()

    def __str__(self):
        return self.nombre
