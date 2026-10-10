from abc import ABC, abstractmethod

class Publicacion(ABC):
    
    LIMITE_CARACTERES = 280
    
    def __init__(self, autor: object, texto:str): 
        if not texto or not texto.strip():
            raise ValueError("El texto no puede estar vacío ni contener solo espacios.")
        if len(texto) > Publicacion.LIMITE_CARACTERES:
            raise ValueError(f"Has superado el límite de {Publicacion.LIMITE_CARACTERES} carácteres")
        self.autor = autor
        self.texto = texto
        self.me_gusta = 0
        
    @abstractmethod
    def __str__(self):
        pass
        
    def dar_me_gusta(self):
        self.me_gusta += 1
        
    @staticmethod
    def extraer_hashtags(texto: str):
        hashtags = []
        
        palabras = texto.split()
        
        for palabra in palabras:
            palabra_limpia = palabra.rstrip(",.!?;:¡¿")
            if palabra_limpia.startswith("#") and len(palabra_limpia) > 1:
                palabra_hashtag = palabra_limpia.lower()
                if palabra_hashtag not in hashtags:
                    hashtags.append(palabra_hashtag)
        
        return hashtags
        
    
    @property
    def hashtags(self):
        return Publicacion.extraer_hashtags(self.texto)
    
class Tweet(Publicacion):
    
    def __str__(self):
        return f"{self.autor.alias}: {self.texto}"
    
class Respuesta(Publicacion):
    
    def __init__(self, autor, texto, original):
        super().__init__(autor, texto)
        self.original = original
        
    def __str__(self):
        return f"{self.autor.alias} {self.original.autor.alias}: {self.texto}"
    
class Retweet(Publicacion):
    def __init__(self, autor, original):
        super().__init__(autor, original.texto)
        self.original = original
        
    def __str__(self):
        return f"{self.autor.alias} 🔄 {self.original}"
    
          
        
        
        
        

            
    
