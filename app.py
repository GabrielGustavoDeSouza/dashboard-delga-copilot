import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard Executivo Delga",
    page_icon="📊",
    layout="wide"
)

# ====================================================================
# HELPERS
# ====================================================================

def safe(v):
    try:
        return float(v)
    except:
        return 0.0

def fmt_mi(v):
    return f"R$ {v/1000000:.2f} Mi"

# ====================================================================
# HEADER
# ====================================================================

st.title("📊 Dashboard Executivo Delga")
st.caption("Versão Copilot Research")

arquivo = st.file_uploader(
    "Selecione a planilha",
    type=["xlsx"]
)

if not arquivo:
    st.info("Faça upload da planilha.")
    st.stop()

excel = pd.ExcelFile(arquivo)

# ====================================================================
# LOCALIZA ABA CONSOLIDADA
# ====================================================================

aba_consolidada = None

for aba in excel.sheet_names:
    if "5 Unidades" in aba:
        aba_consolidada = aba

if aba_consolidada is None:
    st.error("Aba consolidada não encontrada.")
    st.stop()

base = pd.read_excel(
    arquivo,
    sheet_name=aba_consolidada,
    header=None
)

# ====================================================================
# KPIS
# ====================================================================

meta = safe(base.iloc[6,3])
portfolio = safe(base.iloc[6,4])
validado_anual = safe(base.iloc[6,5])
previsto_2026 = safe(base.iloc[6,6])
validado_2026 = safe(base.iloc[6,7])
real = safe(base.iloc[6,10])
extra_dre = safe(base.iloc[6,11])
iniciativas = int(safe(base.iloc[6,14]))

atingimento = 0

if meta > 0:
    atingimento = (real / meta) * 100

# ====================================================================
# CARDS
# ====================================================================

st.subheader("Resumo Executivo")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Meta Grupo",
    fmt_mi(meta)
)

c2.metric(
    "Retorno Previsto",
    fmt_mi(portfolio)
)

c3.metric(
    "Retorno Validado",
    fmt_mi(validado_anual)
)

c4.metric(
    "Iniciativas",
    iniciativas
)

c5,c6,c7,c8 = st.columns(4)

c5.metric(
    "Previsto 2026",
    fmt_mi(previsto_2026)
)

c6.metric(
    "Validado 2026",
    fmt_mi(validado_2026)
)

c7.metric(
    "Retorno Real",
    fmt_mi(real)
)

c8.metric(
    "Extra DRE",
    fmt_mi(extra_dre)
)

# ====================================================================
# GAUGE + FUNIL
# ====================================================================

col1,col2 = st.columns([1,2])

with col1:

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=atingimento,
        number={"suffix":"%"},
        title={"text":"Atingimento"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"darkblue"},
            "steps":[
                {"range":[0,40],"color":"#ffe5e5"},
                {"range":[40,80],"color":"#fff1c9"},
                {"range":[80,100],"color":"#dff5df"}
            ]
        }
    ))

    st.plotly_chart(
        fig_gauge,
        use_container_width=True
    )

with col2:

    df_funil = pd.DataFrame({
        "Etapa":[
            "Meta Grupo",
            "Portfólio",
            "Previsto 2026",
            "Validado",
            "Real"
        ],
        "Valor":[
            meta,
            portfolio,
            previsto_2026,
            validado_2026,
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

# ====================================================================
# META X REAL
# ====================================================================

st.subheader("Meta x Real por Unidade")

dados = []

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

        d = pd.read_excel(
            arquivo,
            sheet_name=aba,
            header=None
        )

        dados.append({
            "Unidade": aba.strip(),
            "Meta": safe(d.iloc[4,0]),
            "Real": safe(d.iloc[4,6])
        })

    except:
        pass

if len(dados) > 0:

    unidade_df = pd.DataFrame(dados)

    fig = go.Figure()

    fig.add_bar(
        x=unidade_df["Unidade"],
        y=unidade_df["Meta"],
        name="Meta"
    )

    fig.add_bar(
        x=unidade_df["Unidade"],
        y=unidade_df["Real"],
        name="Real"
    )

    fig.update_layout(
        barmode="group",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================================================
# TOP PROJETOS
# ====================================================================

st.subheader("Top Projetos")

try:

    top = pd.read_excel(
        arquivo,
        sheet_name="Top 5 Projetos",
        header=None
    )

    st.dataframe(
        top,
        use_container_width=True
    )

except:
    st.warning("Aba Top 5 Projetos não encontrada.")

# ====================================================================
# INSIGHTS
# ====================================================================

st.subheader("Copilot Insights")

gap = meta - real

if portfolio > meta:

    st.success(
        "✅ O portfólio projetado supera a meta anual."
    )

if atingimento < 20:

    st.error(
        f"⚠ Atingimento atual da meta: {atingimento:.1f}%."
    )

if gap > 0:

    st.info(
        f"📌 Gap atual para atingir a meta: {fmt_mi(gap)}"
    )

st.divider()

st.caption(
    "Dashboard experimental gerado automaticamente por Copilot."
)
