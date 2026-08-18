import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Executivo Delga",
    layout="wide"
)

st.title("📊 Dashboard Executivo Delga")

arquivo = st.file_uploader(
    "Selecione a Planilha",
    type=["xlsx"]
)

if arquivo:

    # ---------------------------
    # Aba principal
    # ---------------------------

    master = pd.read_excel(
        arquivo,
        sheet_name="5 Unidades +",
        header=None
    )

    meta = float(master.iloc[6,3])
    previsto = float(master.iloc[6,4])
    validado = float(master.iloc[6,5])
    previsto2026 = float(master.iloc[6,6])
    validado2026 = float(master.iloc[6,7])
    real = float(master.iloc[6,10])
    extra = float(master.iloc[6,11])
    iniciativas = int(master.iloc[6,14])

    atingir = (real/meta)*100

    col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

    col1.metric(
        "Meta Grupo",
        f"R$ {meta/1000000:.2f} Mi"
    )

    col2.metric(
        "Retorno Previsto",
        f"R$ {previsto/1000000:.2f} Mi"
    )

    col3.metric(
        "Retorno Validado",
        f"R$ {validado/1000000:.2f} Mi"
    )

    col4.metric(
        "Previsto 2026",
        f"R$ {previsto2026/1000000:.2f} Mi"
    )

    col5.metric(
        "Validado 2026",
        f"R$ {validado2026/1000000:.2f} Mi"
    )

    col6.metric(
        "Retorno Real",
        f"R$ {real/1000000:.2f} Mi"
    )

    col7.metric(
        "% Meta",
        f"{atingir:.1f}%"
    )

    st.divider()

    # ---------------------------
    # Saving por Unidade
    # ---------------------------

    unidades = pd.DataFrame({
        "Unidade":[
            "Diadema",
            "Ferraz",
            "São Leopoldo",
            "Jarinu",
            "Anchieta",
            "Compras"
        ],
        "Meta":[
            6947000,
            13367000,
            2100000,
            5356000,
            3841000,
            7000000
        ]
    })

    fig = px.bar(
        unidades,
        x="Meta",
        y="Unidade",
        orientation="h",
        title="Meta de Saving por Unidade"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------
    # TOP 5 Projetos
    # ---------------------------

    top5 = pd.read_excel(
        arquivo,
        sheet_name="Top 5 Projetos",
        header=None
    )

    st.subheader("Top Projetos")

    st.dataframe(top5)
