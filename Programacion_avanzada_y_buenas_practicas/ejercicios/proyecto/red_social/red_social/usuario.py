class Usuario:
    def __init__(self, nombre, alias):
        self.nombre = nombre
        self.alias = alias if alias.startswith("@") else f"@{alias}"
        self._seguidos = []
        
    def __str__(self):
        return f"{self.nombre} ({self.alias})"
    
    def __eq__(self, otro):
        return self.alias == otro.alias
    
    def seguir(self,otro):
        if otro == self:
            raise ValueError("Un usuario no puede seguirse a sí mismo")
        if otro in self._seguidos:
            raise ValueError("Ya sigues a este usuario")
        
        self._seguidos.append(otro)
    
    def sigue_a(self, otro):
        return otro in self._seguidos
        
    def a_dict(self):
        return {
            "nombre" : self.nombre,
            "alias" : self.alias
        }
    
    @classmethod
    def desde_dict(cls, datos):
        return cls(datos["nombre"], datos["alias"])
        
    @property
    def numero_seguidos(self):
        return len(self._seguidos)
    
    
        
