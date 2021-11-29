from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Auction(models.Model):
    # Preciso poner: titulo, descripcion, usuario, precio, fecha, categoria, imagen y estado
    # Creo listado de categorias
    CATEGORIAS = (
        ('TEC', 'Tecnologia'),
        ('DEP', 'Deportes'),
        ('ALI', 'Alimentos'),
        ('VES', 'Vestimenta'),
        ('LIB', 'Libros'),
        ('AUT', 'Autos'),
        ('GAM', 'Gaming'),
        ('NON', 'Ninguna'),
        )
    
    titulo = models.CharField(max_length=30, blank = False)
    descripcion = models.CharField(max_length=250, blank = True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    pujaActual = models.FloatField()
    fechaPublicacion = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=3, choices=CATEGORIAS, default="NON")
    imagen = models.ImageField(null = True, blank = True)
    estadoCerrado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.titulo}: vendido por {self.creador} y vale {self.pujaActual}"


class Bid(models.Model):
    #Tengo que poner: quien puja, a que precio, fecha y a que Auction
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    oferta = models.FloatField()
    fechaOferta = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} oferta {self.oferta} por {self.auction}"

class Comentarios(models.Model):
    #Tengo que poner: quien comento, que comento, en que fecha y en que Auction

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True)
    fechaComentario = models.DateTimeField(auto_now_add=True, default=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default=False)

    def __str__(self):
        return f"Comment {self.comentario} en la auction {self.auction} escrito por {self.usuario}"