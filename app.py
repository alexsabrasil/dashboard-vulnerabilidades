import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Vulnerabilidades",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Dashboard de Vulnerabilidades")
st.write(
    "Projeto autoral com dados fictícios para análise de riscos, "
    "priorização e acompanhamento de vulnerabilidades em um contexto de Blue Team."
)

df = pd.read_csv("data/vulnerabilidades.csv")

total = len(df)
criticas = len(df[df["severidade"] == "Crítica"])
altas = len(df[df["severidade"] == "Alta"])
pendentes = len(df[df["status"] == "Pendente"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total", total)
col2.metric("Críticas", criticas)
col3.metric("Altas", altas)
col4.metric("Pendentes", pendentes)

st.divider()

coluna1, coluna2 = st.columns(2)

with coluna1:
    grafico_severidade = px.histogram(
        df,
        x="severidade",
        title="Vulnerabilidades por Severidade"
    )
    st.plotly_chart(grafico_severidade, use_container_width=True)

with coluna2:
    grafico_status = px.histogram(
        df,
        x="status",
        title="Vulnerabilidades por Status"
    )
    st.plotly_chart(grafico_status, use_container_width=True)

grafico_cvss = px.scatter(
    df,
    x="ativo",
    y="cvss",
    color="severidade",
    size="cvss",
    title="Pontuação CVSS por Ativo"
)

st.plotly_chart(grafico_cvss, use_container_width=True)

st.subheader("Base de Vulnerabilidades")
st.dataframe(df, use_container_width=True)