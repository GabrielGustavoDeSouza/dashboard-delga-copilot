import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    "unidade":[
        "Diadema",
        "Ferraz",
        "São Leopoldo",
        "Jarinu",
        "Anchieta",
        "Compras"
    ],
    "saving":[
        997267,
        1892595,
        1158700,
        463507,
        331444,
        1282436
    ]
})

fig = px.bar(
    df,
    x="saving",
    y="unidade",
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)
