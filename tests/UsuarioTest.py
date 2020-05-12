import unittest
from models.Usuario import Usuario


class UsuarioTest(unittest.TestCase):

    def testLogin(self):
        usuario = Usuario(1, 'admin', 'usuario', '1234')
        resultado = usuario.login('usuario', '1234')

        self.assertNotEqual(resultado, False, 'credenciales incorrectas')
        self.assertEqual(resultado, True, 'credenciales correctas')
