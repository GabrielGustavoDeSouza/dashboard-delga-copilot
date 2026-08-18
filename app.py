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

if arquivo is not None:

    excel = pd.ExcelFile(arquivo)

    st.success("Planilha carregada com sucesso")

    aba_grupo = None

    for aba in excel.sheet_names:
        if "5 Unidades" in aba:
            aba_grupo = aba
            break

    if aba_grupo is None:
        st.error(
            f"Aba principal não encontrada. Abas localizadas: {excel.sheet_names}"
        )
        st.stop()

    grupo = pd.read_excel(
        arquivo,
        sheet_name=aba_grupo,
        header=None
    )

    try:

        meta = float(grupo.iloc[6,3])
        previsto = float(grupo.iloc[6,4])
        validado = float(grupo.iloc[6,5])
        previsto2026 = float(grupo.iloc[6,6])
        validado2026 = float(grupo.iloc[6,7])
        real = float(grupo.iloc[6,10])
        extra = float(grupo.iloc[6,11])
        iniciativas = int(grupo.iloc[6,14])

    except Exception as e:
        st.error(f"Erro lendo os KPIs da planilha: {e}")
        st.stop()

    percentual = (real / meta) * 100 if meta > 0 else 0

    st.subheader("Resumo Executivo")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Meta Grupo",
        f"R$ {meta/1000000:.2f} Mi"
    )

    c2.metric(
        "Retorno Previsto",
        f"R$ {previsto/1000000:.2f} Mi"
    )

    c3.metric(
        "Retorno Validado",
        f"R$ {validado/1000000:.2f} Mi"
    )

    c4.metric(
        "Iniciativas",
        f"{iniciativas}"
    )

    c5,c6,c7,c8 = st.columns(4)

    c5.metric(
        "Previsto 2026",
        f"R$ {previsto2026/1000000:.2f} Mi"
    )

    c6.metric(
        "Validado 2026",
        f"R$ {validado2026/1000000:.2f} Mi"
    )

    c7.metric(
        "Retorno Real",
        f"R$ {real/1000000:.2f} Mi"
    )

    c8.metric(
        "Extra DRE",
        f"R$ {extra/1000000:.2f} Mi"
    )

    st.divider()

    col_esq, col_dir = st.columns([1, 2])

    with col_esq:

        fig_gauge = go.Figure()

        fig_gauge.add_trace(go.Indicator(
            mode="gauge+number",
            value=percentual,
            number={"suffix":"%"},
            title={"text":"Atingimento da Meta"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"#0E4C92"},
                "steps":[
                    {"range[1, .F":[0,40],"color":"#ffdede                  {"range":[40,80],"color":"#fff0c7"},
                    {"range":[80,100],"color":"#dff5df"}
                ]
            }
        ))

        st.plotly_chart(
            fig_gauge,
            use_container_width=True
        )

    with col_dir:

        df_funil = pd.DataFrame({
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
            df_funil,
            x="Valor",
            y="Etapa",
            color="Etapa"
        )

        st.plotly_chart(
            fig_funil,
            use_container_width=True
        )

    st.divider()

    unidades = []

    abas_unidades = [
        "Diadema",
        "Ferraz",
        "Jarinu",
        "São Leopoldo",
        "Anchieta",
        "Compras "
    ]

    for aba in abas_unidades:

        try:

            df = pd.read_excel(
                arquivo,
                sheet_name=aba,
                header=None
            )

            unidades.append({
                "Unidade": aba.strip(),
                "Meta": float(df.iloc[4,0]),
                "Real": float(df.iloc[4,6])
            })

        except:
            pass

    if len(unidades) > 0:

        df_unidades = pd.DataFrame(unidades)

        st.subheader("Meta x Real por Unidade")

        fig_unidades = go.Figure()

        fig_unidades.add_bar(
            name="Meta",
            x=df_unidades["Unidade"],
            y=df_unidades["Meta"]
        )

        fig_unidades.add_bar(
            name="Real",
            x=df_unidades["Unidade"],
            y=df_unidades["Real"]
        )

        fig_unidades.update_layout(
            barmode="group"
        )

        st.plotly_chart(
            fig_unidades,
            use_container_width=True
        )

    st.divider()

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
        st.warning("Não foi possível carregar Top 5 Projetos.")

    st.divider()

    st.subheader("Copilot Insights")

    gap = meta - real

    if previsto > meta:
        st.success(
            "✅ O portfólio previsto supera a meta anual do grupo."
        )

    if percentual < 20:
        st.error(
            f"⚠ Atingimento da meta está em apenas {percentual:.1f}%."
        )

    st.info(
        f"📌 Gap atual para atingir a meta: R$ {gap/1000000:.2f} Mi"
    )

else:

    st.info(
        "Faça upload da planilha para iniciar a análise."
    )
