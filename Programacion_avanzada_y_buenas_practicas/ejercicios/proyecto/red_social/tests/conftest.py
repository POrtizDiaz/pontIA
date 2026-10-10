import pytest
from red_social.red import RedSocial
from red_social.publicacion import Tweet
from red_social.usuario import Usuario

@pytest.fixture
def ana():
    return Usuario("Ana", "@ana")

@pytest.fixture
def luis():
    return Usuario("Luis", "@luis")

@pytest.fixture
def tweet(ana):
    return Tweet(ana, "Hola a todos #python #pytest")

@pytest.fixture
def red():
    r = RedSocial()
    r.registrar("Ana", "@ana")
    r.registrar("Luis", "@luis")
    r.registrar("Marta", "@marta")
    r["@luis"].seguir(r["@ana"])
    return r