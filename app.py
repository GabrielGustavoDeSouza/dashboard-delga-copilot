import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Delga Copilot",
    layout="wide"
)

st.title("📊 Dashboard Delga Copilot")

arquivo = st.file_uploader(
    "Selecione uma planilha Excel",
    type=["xlsx"]
)

if arquivo:

    excel = pd.ExcelFile(arquivo)

    st.success("Planilha carregada com sucesso")

    aba = st.selectbox(
        "Escolha uma aba",
        excel.sheet_names
    )

    df = pd.read_excel(
        excel,
        sheet_name=aba
    )

    st.subheader("Prévia dos Dados")

    st.dataframe(df)

    st.subheader("Resumo")

    c1, c2, c3 = st.columns(3)

    c1.metric("Linhas", len(df))
    c2.metric("Colunas", len(df.columns))
    c3.metric("Aba", aba)

else:

    st.info("Envie um arquivo Excel para iniciar a análise.")
