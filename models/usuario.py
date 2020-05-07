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