import pandas as pd

ARQUIVO = "Controle_Indicadores_Delga_2026_v360 (48).xlsx"

def carregar_dados():
    return pd.read_excel(
        ARQUIVO,
        sheet_name=None,
        engine="openpyxl"
    )
