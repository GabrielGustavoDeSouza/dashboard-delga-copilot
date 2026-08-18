import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

if arquivo:

    excel = pd.ExcelFile(arquivo)

    st.success("Planilha carregada")

    # ==========================
    # DASHBOARD GRUPO
    # ==========================

    aba_grupo = None

    for aba in excel.sheet_names:
        if "5 Unidades" in aba:
            aba_grupo = aba
            break

    if aba_grupo is None:
        st.error("Aba de consolidação não encontrada.")
        st.stop()

    grupo = pd.read_excel(
        arquivo,
        sheet_name=aba_grupo,
        header=None
    )

    meta = float(grupo.iloc[6,3])
    previsto = float(grupo.iloc[6,4])
    validado = float(grupo.iloc[6,5])
    previsto2026 = float(grupo.iloc[6,6])
    validado2026 = float(grupo.iloc[6,7])
    real = float(grupo.iloc[6,10])
    extra = float(grupo.iloc[6,11])
    iniciativas = int(grupo.iloc[6,14])

    col1,col2,col3,col4 = st.columns(4)

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
        "Iniciativas",
        iniciativas
    )

    col5,col6,col7,col8 = st.columns(4)

    col5.metric(
        "Previsto 2026",
        f"R$ {previsto2026/1000000:.2f} Mi"
    )

    col6.metric(
        "Validado 2026",
        f"R$ {validado2026/1000000:.2f} Mi"
    )

    col7.metric(
        "Retorno Real",
        f"R$ {real/1000000:.2f} Mi"
    )

    col8.metric(
        "Extra DRE",
        f"R$ {extra/1000000:.2f} Mi"
    )

    st.divider()

    # ==========================
    # GAUGE META
    # ==========================

    percentual = (real / meta) * 100

    g1,g2 = st.columns([2,3])

    with g1:

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=percentual,
            number={'suffix': "%"},
            title={'text': "Atingimento da Meta"},
            gauge={
                'axis': {'range': [0,100]},
                'bar': {'color': '#0E4C92'},
                'steps': [
                    {'range':[[2={'suffix': {'color': '#0E4C92'},           {'range':[40,80],'color':'#fff4d6'},
                    {'range':[80,100],'color':'#e8f5e9'}
                ]
            }
        ))

        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )

    with g2:

        funnel = pd.DataFrame({
            "Etapa":[
                "Meta Grupo",
                "Retorno Previsto",
                "Retorno Validado",
                "Retorno Real"
            ],
            "Valor":[
                meta,
                previsto,
                validado,
                real
            ]
        })

        fig_funil = px.funnel(
            funnel,
            x="Valor",
            y="Etapa"
        )

        st.plotly_chart(
            fig_funil,
            use_container_width=True
        )

    st.divider()

    # ==========================
    # UNIDADES
    # ==========================

    unidades = []

    abas = [
        "Diadema",
        "Ferraz",
        "Jarinu",
        "São Leopoldo",
        "Anchieta",
        "Compras "
    ]

    for aba in abas:

        try:

            df = pd.read_excel(
                arquivo,
                sheet_name=aba,
                header=None
            )

            unidades.append(
                {
                    "Unidade": aba.strip(),
                    "Meta": float(df.iloc[4,0]),
                    "Real": float(df.iloc[4,6])
                }
            )

        except:
            pass

    unidades = pd.DataFrame(unidades)

    if len(unidades)>0:

        fig = go.Figure()

        fig.add_bar(
            name="Meta",
            x=unidades["Unidade"],
            y=unidades["Meta"]
        )

        fig.add_bar(
            name="Real",
            x=unidades["Unidade"],
            y=unidades["Real"]
        )

        st.subheader("Meta x Real por Unidade")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ==========================
    # TOP 5 PROJETOS
    # ==========================

    try:

        top = pd.read_excel(
            arquivo,
            sheet_name="Top 5 Projetos",
            header=None
        )

        st.subheader("Top 5 Projetos")

        st.dataframe(
            top,
            use_container_width=True
        )

    except:

        st.warning(
            "Aba Top 5 Projetos não encontrada."
        )

    st.divider()

    # ==========================
    # INSIGHTS
    # ==========================

    st.subheader("Copilot Insights")

    if percentual < 20:
        st.error(
            f"Atingimento da meta em apenas {percentual:.1f}%."
        )

    if previsto > meta:
        st.success(
            "Portfólio previsto supera a meta anual."
        )

    gap = meta - real

    st.info(
        f"Gap atual para atingir a meta: R$ {gap/1000000:.2f} Mi"
    )

else:

    st.info(
        "Faça upload da planilha para iniciar."
    )
