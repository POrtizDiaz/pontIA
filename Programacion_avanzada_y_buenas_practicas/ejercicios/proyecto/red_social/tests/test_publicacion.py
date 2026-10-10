import pytest
from red_social.publicacion import Publicacion, Tweet

@pytest.mark.parametrize(
    "texto",
    [
        "",
        "   ",
        "a" * 281,
    ],
)
def test_texto_invalido_lanza_error(ana, texto):
    with pytest.raises(ValueError):
        Tweet(ana, texto)

@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Un texto sin hashtags", []),
        ("Hola #Python #PYTEST", ["#python", "#pytest"]),
        ("#python y otra vez #python", ["#python"]),
        ("Me gusta #python, y mucho #pytest!", ["#python", "#pytest"]),
    ],
)
def test_extraer_hashtags(texto, esperado):
    assert Publicacion.extraer_hashtags(texto) == esperado