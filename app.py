import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Executivo Delga",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Executivo Delga")

arquivo = st.file_uploader(
    "Selecione a planilha",
    type=["xlsx"]
)

if arquivo:

    excel = pd.ExcelFile(arquivo)

    st.success("Planilha carregada com sucesso")

    aba = st.selectbox(
        "Selecione uma aba",
        excel.sheet_names
    )

    df = pd.read_excel(
        arquivo,
        sheet_name=aba,
        header=None
    )

    st.subheader("Dados Brutos")

    st.dataframe(df)

    try:

        meta = "R$ 50,32 Mi"
        realizado = "R$ 0"
        atingimento = "0%"
        gap = "R$ 50,32 Mi"

        c1,c2,c3,c4 = st.columns(4)

        c1.metric(
            "Meta Anual",
            meta
        )

        c2.metric(
            "Realizado",
            realizado
        )

        c3.metric(
            "% Atingimento",
            atingimento
        )

        c4.metric(
            "Gap",
            gap
        )

    except:
        pass

else:

    st.info(
        "Faça upload da planilha para iniciar."
    )
