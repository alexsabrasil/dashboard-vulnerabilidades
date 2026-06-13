import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Vulnerabilidades",
    page_icon="🛡️",
    layout="wide"
)

df = pd.read_csv("data/vulnerabilidades.csv")

df["data_descoberta"] = pd.to_datetime(df["data_descoberta"])
df["data_correcao"] = pd.to_datetime(df["data_correcao"], errors="coerce")
df["dias_correcao"] = (df["data_correcao"] - df["data_descoberta"]).dt.days

pagina = st.sidebar.radio(
    "Menu",
    ["Sobre o Projeto", "Dashboard"]
)

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

if pagina == "Dashboard":
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

    total = len(df_filtrado)
    criticas = len(df_filtrado[df_filtrado["severidade"] == "Crítica"])
    altas = len(df_filtrado[df_filtrado["severidade"] == "Alta"])
    pendentes = len(df_filtrado[df_filtrado["status"] == "Pendente"])
    corrigidas = len(df_filtrado[df_filtrado["status"] == "Corrigida"])

    mttr = round(df_filtrado["dias_correcao"].mean(), 1)

    hoje = pd.Timestamp.now()

    criticas_pendentes = df_filtrado[
        (df_filtrado["severidade"] == "Crítica") &
        (df_filtrado["status"] != "Corrigida")
    ]

    fora_sla = len(
        criticas_pendentes[
            (hoje - criticas_pendentes["data_descoberta"]).dt.days > 15
        ]
    )

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    col1.metric("Total", total)
    col2.metric("Críticas", criticas)
    col3.metric("Altas", altas)
    col4.metric("Pendentes", pendentes)
    col5.metric("Corrigidas", corrigidas)
    col6.metric("MTTR Médio", f"{mttr} dias")
    col7.metric("Fora de SLA", fora_sla)

    st.divider()

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        grafico_severidade = px.histogram(
            df_filtrado,
            x="severidade",
            title="Vulnerabilidades por Severidade"
        )
        st.plotly_chart(grafico_severidade, use_container_width=True)

    with coluna2:
        grafico_status = px.histogram(
            df_filtrado,
            x="status",
            title="Vulnerabilidades por Status"
        )
        st.plotly_chart(grafico_status, use_container_width=True)

    st.divider()

    coluna3, coluna4 = st.columns(2)

    with coluna3:
        grafico_responsavel = px.histogram(
            df_filtrado,
            x="responsavel",
            color="severidade",
            title="Vulnerabilidades por Responsável"
        )
        st.plotly_chart(grafico_responsavel, use_container_width=True)

    with coluna4:
        grafico_ativos = px.histogram(
            df_filtrado,
            x="ativo",
            color="severidade",
            title="Top Ativos com Vulnerabilidades"
        )
        st.plotly_chart(grafico_ativos, use_container_width=True)

    grafico_cvss = px.scatter(
        df_filtrado,
        x="ativo",
        y="cvss",
        color="severidade",
        size="cvss",
        title="Pontuação CVSS por Ativo"
    )

    st.plotly_chart(grafico_cvss, use_container_width=True)

    st.subheader("Pesquisar Vulnerabilidade")

    busca = st.text_input("Pesquisar por CVE ou Ativo")

    if busca:
        df_filtrado = df_filtrado[
            df_filtrado["ativo"].str.contains(busca, case=False, na=False) |
            df_filtrado["cve"].str.contains(busca, case=False, na=False)
        ]

    st.subheader("Top Vulnerabilidades Críticas")

    top_criticas = (
        df_filtrado
        .sort_values(by="cvss", ascending=False)
        .head(10)
    )

    st.dataframe(
        top_criticas[["cve", "ativo", "severidade", "cvss", "status", "responsavel"]],
        use_container_width=True
    )

    st.subheader("Base de Vulnerabilidades")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.title("Sobre o Projeto")

    st.write(
        """
        Este projeto foi desenvolvido para demonstrar, de forma prática, conceitos de
        Segurança da Informação, Blue Team e Gestão de Vulnerabilidades.

        A base utilizada é fictícia e foi criada exclusivamente para fins educacionais
        e de portfólio, sem uso de dados reais ou informações de terceiros.
        """
    )

    st.subheader("Conceitos aplicados")

    st.write(
        """
        - Gestão de Vulnerabilidades
        - Blue Team
        - Segurança da Informação
        - Análise de Riscos
        - CVSS
        - MTTR
        - SLA de correção
        - Indicadores de Segurança
        """
    )

    st.subheader("Tecnologias utilizadas")

    st.write(
        """
        - Python
        - Streamlit
        - Pandas
        - Plotly
        - Git
        - GitHub
        """
    )
    
    st.subheader("Objetivos do Projeto")

st.write("""
• Demonstrar conhecimentos em Gestão de Vulnerabilidades.
• Aplicar conceitos de Blue Team.
• Construir indicadores de segurança.
• Praticar análise de riscos utilizando CVSS.
• Desenvolver dashboards interativos com Python.
""")

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; color:#808080; font-size:13px;'>
    © 2026 Alê Tavares | Dashboard de Vulnerabilidades<br>
    Desenvolvido com Python, Streamlit e Plotly para fins de estudo, demonstração técnica e portfólio profissional.
    Contato: <a href='https://www.linkedin.com/in/aletavaress/' target='_blank'>LinkedIn</a> | <a href='@alemdoslogs' target='_blank'>Instagram</a>
    </div>
    """,
    unsafe_allow_html=True
)