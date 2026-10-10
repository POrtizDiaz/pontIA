from collections import Counter
import json
from red_social.usuario import Usuario


class RedSocial:
    def __init__(self):
        self.usuarios = {}
        self.publicaciones = []
        
    def __len__(self):
        return len(self.usuarios)
    
    def __iter__(self):
        return iter(sorted(self.usuarios.values(), key=lambda u: u.alias))
    
    def __contains__(self, alias):
        return alias in self.usuarios
    
    def __getitem__(self, alias):
        return self.usuarios[alias]
        
    def anadir(self, usuario:object):
        
        if usuario.alias in self.usuarios:
            raise ValueError(f"Este usuario ya está registrado")
        
        self.usuarios[usuario.alias] = usuario
        
        return usuario
    
    def registrar(self, nombre, alias):
        
        usuario = Usuario(nombre, alias)
        
        return self.anadir(usuario)
        
        
    def publicar(self, publicacion:object):
        
        if publicacion.autor.alias not in self.usuarios:
            raise ValueError (f"Este usuario no existe en la plataforma")
        
        self.publicaciones.append(publicacion)
        
        return publicacion
        
    def timeline(self, usuario:object):
        publicaciones_seguidos = []
        for publicaciones in self.publicaciones:
            if publicaciones.autor in usuario._seguidos:
                publicaciones_seguidos.append(publicaciones)
        
        return publicaciones_seguidos[::-1]
    
    def tendencias(self, n=3):
        hashtags_mas_usados = []
        
        for publicacion in self.publicaciones:
           hashtags_mas_usados.extend(publicacion.hashtags)
           
        return Counter(hashtags_mas_usados).most_common(n)
    
    def mostrar_timeline(self, alias):
        usuario = self[alias]

        print(f"\nTimeline de {usuario}:")

        for publicacion in self.timeline(usuario):
            print(publicacion)
            
    @classmethod
    def desde_json(cls, ruta):

      with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)

      red = cls()

      for datos_usuario in datos.get("usuarios", []):
        usuario = Usuario.desde_dict(datos_usuario)
        red.anadir(usuario)

      for alias_seguidor, alias_perseguido in datos.get("seguimientos", []):
        seguidor = red[alias_seguidor]
        perseguido = red[alias_perseguido]
        seguidor.seguir(perseguido)

      return red
    
    
    