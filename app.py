import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Executivo Delga",
    page_icon="📊",
    layout="wide"
)

def safe(v):
    try:
        if pd.isna(v):
            return 0
        return float(v)
    except:
        return 0

def moeda(v):
    return f"R$ {v:,.0f}".replace(",", ".")

st.title("📊 Dashboard Executivo Delga")

arquivo = st.file_uploader(
    "Selecione a planilha",
    type=["xlsx"]
)

if arquivo is None:
    st.stop()

excel = pd.ExcelFile(arquivo)

aba_consolidada = None

for aba in excel.sheet_names:
    if "5 Unidades" in aba:
        aba_consolidada = aba
        break

if aba_consolidada is None:
    st.error("Aba consolidada não encontrada.")
    st.write(excel.sheet_names)
    st.stop()

base = pd.read_excel(
    arquivo,
    sheet_name=aba_consolidada,
    header=None
)

st.success("Planilha carregada")

try:

    meta = safe(base.iloc[6,3])
    portfolio = safe(base.iloc[6,4])
    validado_anual = safe(base.iloc[6,5])
    previsto2026 = safe(base.iloc[6,6])
    validado2026 = safe(base.iloc[6,7])

    real = safe(base.iloc[6,10])
    extra = safe(base.iloc[6,11])

    iniciativas = safe(base.iloc[6,14])

except Exception as e:

    st.error(f"Erro lendo KPIs: {e}")
    st.dataframe(base.head(15))
    st.stop()

atingimento = 0

if meta > 0:
    atingimento = (real / meta) * 100

st.subheader("Resumo Executivo")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Meta Grupo",
    moeda(meta)
)

c2.metric(
    "Portfolio",
    moeda(portfolio)
)

c3.metric(
    "Validado Anual",
    moeda(validado_anual)
)

c4.metric(
    "Iniciativas",
    int(iniciativas)
)

c5,c6,c7,c8 = st.columns(4)

c5.metric(
    "Previsto 2026",
    moeda(previsto2026)
)

c6.metric(
    "Validado 2026",
    moeda(validado2026)
)

c7.metric(
    "Retorno Real",
    moeda(real)
)

c8.metric(
    "Extra DRE",
    moeda(extra)
)

st.divider()

col1,col2 = st.columns([1,2])

with col1:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=atingimento,
            number={"suffix":"%"},
            title={"text":"Atingimento"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"darkblue"},
                "steps":[
                    {"range":[0,40],"color":"#ffdddd"},
                    {"range":[40,80],"color":"#fff4cc"},
                    {"range":[80,100],"color":"#ddffdd"}
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    funil = pd.DataFrame({
        "Etapa":[
            "Meta",
            "Portfolio",
            "Previsto 2026",
            "Validado",
            "Real"
        ],
        "Valor":[
            meta,
            portfolio,
            previsto2026,
            validado2026,
            real
        ]
    })

    fig2 = px.funnel(
        funil,
        x="Valor",
        y="Etapa",
        color="Etapa"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

dados_unidades = []

for aba in [
    "Diadema",
    "Ferraz",
    "Jarinu",
    "São Leopoldo",
    "Anchieta",
    "Compras "
]:

    try:

        df = pd.read_excel(
            arquivo,
            sheet_name=aba,
            header=None
        )

        dados_unidades.append({
            "Unidade": aba.strip(),
            "Meta": safe(df.iloc[4,0]),
            "Real": safe(df.iloc[4,6])
        })

    except:
        pass

if len(dados_unidades):

    uni = pd.DataFrame(dados_unidades)

    fig3 = go.Figure()

    fig3.add_bar(
        x=uni["Unidade"],
        y=uni["Meta"],
        name="Meta"
    )

    fig3.add_bar(
        x=uni["Unidade"],
        y=uni["Real"],
        name="Real"
    )

    fig3.update_layout(
        title="Meta x Real por Unidade",
        barmode="group",
        height=450
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

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

st.subheader("Insights")

gap = meta - real

if portfolio > meta:
    st.success(
        "✅ O portfólio supera a meta do grupo."
    )

if atingimento < 20:
    st.warning(
        f"⚠ Atingimento atual: {atingimento:.1f}%"
    )

st.info(
    f"Gap para meta: {moeda(gap)}"
)

st.subheader("Abas encontradas")

st.write(excel.sheet_names)
