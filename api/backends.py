from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Un backend de autenticación personalizado que permite a los usuarios 
    iniciar sesión usando su dirección de correo electrónico y contraseña.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Intenta autenticar un usuario basándose en su correo electrónico y contraseña.
        
        Parameters:
        - request: HttpRequest object
        - username: string, el correo electrónico del usuario
        - password: string, la contraseña del usuario
        
        Return:
        - Retorna un objeto User si la autenticación es exitosa, None en caso contrario.
        """
        
        UserModel = get_user_model()  # Obtener el modelo de usuario actualmente activo.
        
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        try:
            # Convertimos el correo a minúsculas para evitar problemas de case sensitivity.
            user = UserModel.objects.get(email=username.lower())
        except UserModel.DoesNotExist:
            UserModel().set_password(password)  # Evitar ataques de temporización.
            return
        
        # Verificar si la contraseña es correcta y si el usuario está activo.
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        """
        Obtener un objeto usuario basado en su user_id.
        
        Parameters:
        - user_id: int, el ID del usuario
        
        Return:
        - Retorna un objeto User si el usuario existe, None en caso contrario.
        """
        
        UserModel = get_user_model()  # Obtener el modelo de usuario actualmente activo.
        
        try:
            # Intenta obtener un usuario que coincida con el user_id proporcionado.
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
