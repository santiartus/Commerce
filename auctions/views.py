from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.deletion import RestrictedError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.utils.regex_helper import Choice

from .models import User, Auction, Comentarios, Bid

class CrearListadoForm(forms.ModelForm):
    titulo = forms.CharField(label="Titulo", max_length=15, required=True)
    descripcion = forms.CharField(label="Descripcion")
    imagen = forms.URLField(label="URL de la Imagen", required=True)
    pujaActual = forms.FloatField(label="Precio", required=True)
    categoria = forms.ChoiceField(required=True, choices =Auction.CATEGORIAS)

    class Meta:
        model = Auction
        fields = ["titulo", "descripcion", "categoria", "imagen", "pujaActual"]

def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def crear_listado(request):
    if request.method == "POST":
        form = CrearListadoForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data["titulo"]
            descripcion = form.cleaned_data["descripcion"]
            url_imagen = form.cleaned_data["url_imagen"]
            categoria = form.cleaned_data["categoria"]
            pujaActual = form.cleaned_data["precio"]

            auction = Auction(
                creador = User.objects.get(pk=request.user.id),
                titulo = titulo,
                descripcion = descripcion,
                imagen = url_imagen,
                categoria = categoria,
                pujaActual = pujaActual,
            )
            auction.save()
        else:
            return render(request, "auctions/crear_listado.html", {
                "form": form
            })   

    return render(request, "auctions/crear_listado.html", {
        "form": CrearListadoForm(),
    })
