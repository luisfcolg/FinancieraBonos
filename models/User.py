import logging
import traceback

logging.basicConfig(level=logging.DEBUG, filename='events.log')


class User:
    def __init__(self, id, role, username, password):
        self.id = id
        self.role = role
        self.username = username
        self.password = password

    def getId(self):
        return self.id

    def getRole(self):
        return self.role

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def login(self, username, password):
        """
            This function will be used to validate the user
            :param username: text string
            :param password: text string
            :return: boolean, true if credentials are valid, false if they are invalid
        """
        try:
            if self.username == username and self.password == password:
                logging.debug("Username {} and password {} are validated".format(username, password))
                return True
            return False
        except Exception as ex:
            message = 'There was an error of authentication - {}\n{}'.format(ex, traceback.format_exc())
            logging.error(message)
