import pandas as pd

ARQUIVO = "data/Controle_Indicadores_Delga_2026.xlsx"

def carregar_dados():
    return pd.read_excel(
        ARQUIVO,
        sheet_name=None,
        engine="openpyxl"
    )
