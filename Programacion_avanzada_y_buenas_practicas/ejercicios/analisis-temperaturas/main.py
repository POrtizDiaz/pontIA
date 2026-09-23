
import pandas as pd

def temperatura_media_por_ciudad(df):
    return df.groupby("ciudad")["temperatura"].mean().round(1)

def main():
    df = pd.DataFrame({
        "ciudad": ["Madrid", "Madrid", "Sevilla", "Sevilla", "Bilbao", "Bilbao"],
        "temperatura": [28.0, 32.0, 36.0, 40.0, 21.0, 24.0],
    })
    print(f"pandas {pd.__version__}")
    print("Temperatura media por ciudad:")
    print(temperatura_media_por_ciudad(df).to_string())

if __name__ == "__main__":
    main()