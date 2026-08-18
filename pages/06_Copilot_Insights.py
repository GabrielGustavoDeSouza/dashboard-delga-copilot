if percentual < 20:
    st.warning(
        "⚠ Unidade abaixo de 20% da meta anual."
    )

if percentual > 50:
    st.success(
        "✅ Unidade acima de 50% da meta."
    )
