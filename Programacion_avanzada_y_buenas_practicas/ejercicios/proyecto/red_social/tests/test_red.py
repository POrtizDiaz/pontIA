from red_social.publicacion import Retweet
from red_social.red import RedSocial

def test_retweet_comparte_el_texto_del_original(tweet, luis):
    retweet = Retweet(luis, tweet)
    assert retweet.original is tweet
    assert retweet.texto == tweet.texto
    assert retweet.hashtags == tweet.hashtags
    assert retweet.autor == luis

def test_timeline_solo_tiene_publicaciones_de_los_seguidos(red, tweet):
    red.publicar(tweet)
    luis = red["@luis"]
    ana = red["@ana"]
    timeline_luis = red.timeline(luis)
    assert len(timeline_luis) == 1
    assert timeline_luis[0] is tweet
    assert len(red.timeline(ana)) == 0

def test_desde_json_construye_usuarios_y_seguimientos(mocker):
    datos_falsos = {
        "usuarios": [
            {"nombre": "Ana", "alias": "@ana"},
            {"nombre": "Luis", "alias": "@luis"},
        ],
        "seguimientos": [["@luis", "@ana"]],
    }
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="{}"))
    mocker.patch("json.load", return_value=datos_falsos)
    red = RedSocial.desde_json("datos/usuarios.json")
    mock_open.assert_called_once_with("datos/usuarios.json", encoding="utf-8")
    assert len(red) == 2
    assert red["@luis"].sigue_a(red["@ana"]) is True