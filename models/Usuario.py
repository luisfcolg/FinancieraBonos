import logging
import traceback

logging.basicConfig(level=logging.DEBUG, filename='events.log')


class Usuario:
    def __init__(self, id, rol, usuario, contrasena):
        self.id = id
        self.rol = rol
        self.usuario = usuario
        self.contrasena = contrasena

    def getId(self):
        return self.id

    def getRol(self):
        return self.rol

    def getUsuario(self):
        return self.usuario

    def getContrasena(self):
        return self.contrasena

    def login(self, usuario, contrasena):
        """
            Esta función será usada para validar al usuario
            :param usuario: cadena de texto
            :param contrasena: cadena de texto
            :return: booleano, verdadero si las credenciales son válidas, falso si son inválidas
        """
        try:
            if self.usuario == usuario and self.contrasena == contrasena:
                logging.debug("Se validan el usuario {} y la contraseña {}".format(usuario, contrasena))
                return True
            return False
        except Exception as ex:
            message = 'Ocurrió un error al autentificar - {}\n{}'.format(ex, traceback.format_exc())
            logging.error(message)
