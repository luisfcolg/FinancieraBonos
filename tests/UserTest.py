import unittest
from models.User import User


class UserTest(unittest.TestCase):

    def testLogin(self):
        user = User(1, 'admin', 'usuario', '1234')
        result = user.login('usuario', '1234')

        self.assertNotEqual(result, False, 'Valid credentials')
        self.assertEqual(result, True, 'Valid credentials')
