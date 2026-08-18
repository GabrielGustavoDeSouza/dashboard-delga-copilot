import streamlit as st

st.set_page_config(
    page_title="Dashboard Executivo Delga",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Executivo Delga")

arquivo = st.file_uploader(
    "Selecione a planilha Excel",
    type=["xlsx"]
)

if arquivo is not None:
    st.success("Planilha carregada com sucesso.")
    st.write("Nome do arquivo:", arquivo.name)
else:
    st.info("Faça upload da planilha.")
