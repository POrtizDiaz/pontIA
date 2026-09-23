import pandas as pd
from main import temperatura_media_por_ciudad

def test_temperatura_media():
    df = pd.DataFrame({
        "ciudad": ["Madrid", "Madrid", "Sevilla"],
        "temperatura": [28.0, 32.0, 40.0],
    })
    resultado = temperatura_media_por_ciudad(df)
    assert resultado["Madrid"] == 30.0
    assert resultado["Sevilla"] == 40.0
