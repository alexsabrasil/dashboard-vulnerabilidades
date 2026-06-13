import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Vulnerabilidades",
    page_icon="🛡️",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center;'>
    🛡️ Dashboard de Vulnerabilidades
    </h1>
    """,
    unsafe_allow_html=True
)

st.write(
    "Projeto autoral com dados fictícios para análise de riscos, "
    "priorização e acompanhamento de vulnerabilidades em um contexto de Blue Team."
)

df = pd.read_csv("data/vulnerabilidades.csv")

df["data_descoberta"] = pd.to_datetime(df["data_descoberta"])
df["data_correcao"] = pd.to_datetime(df["data_correcao"], errors="coerce")

df["dias_correcao"] = (df["data_correcao"] - df["data_descoberta"]).dt.days

mttr = round(df["dias_correcao"].mean(), 1)
corrigidas = len(df[df["status"] == "Corrigida"])

st.sidebar.title("Filtros")

filtro_severidade = st.sidebar.multiselect(
    "Severidade",
    options=df["severidade"].unique(),
    default=df["severidade"].unique()
)

filtro_status = st.sidebar.multiselect(
    "Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

filtro_sistema = st.sidebar.multiselect(
    "Sistema",
    options=df["sistema"].unique(),
    default=df["sistema"].unique()
)

filtro_responsavel = st.sidebar.multiselect(
    "Responsável",
    options=df["responsavel"].unique(),
    default=df["responsavel"].unique()
)

df_filtrado = df[
    (df["severidade"].isin(filtro_severidade)) &
    (df["status"].isin(filtro_status)) &
    (df["sistema"].isin(filtro_sistema)) &
    (df["responsavel"].isin(filtro_responsavel))
]

total = len(df_filtrado)
criticas = len(df_filtrado[df_filtrado["severidade"] == "Crítica"])
altas = len(df_filtrado[df_filtrado["severidade"] == "Alta"])
pendentes = len(df_filtrado[df_filtrado["status"] == "Pendente"])

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total", total)
col2.metric("Críticas", criticas)
col3.metric("Altas", altas)
col4.metric("Pendentes", pendentes)
col5.metric("Corrigidas", corrigidas)
col6.metric("MTTR Médio", f"{mttr} dias")

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

st.divider()

coluna3, coluna4 = st.columns(2)

with coluna3:
    grafico_responsavel = px.histogram(
        df_filtrado,
        x="responsavel",
        title="Vulnerabilidades por Responsável"
    )
    st.plotly_chart(grafico_responsavel, use_container_width=True)

with coluna4:
    grafico_ativos = px.histogram(
        df_filtrado,
        x="ativo",
        title="Top Ativos com Vulnerabilidades"
    )
    st.plotly_chart(grafico_ativos, use_container_width=True)

st.plotly_chart(grafico_cvss, use_container_width=True)

st.subheader("Base de Vulnerabilidades")
st.dataframe(df_filtrado, use_container_width=True)