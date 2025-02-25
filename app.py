#-------------------
# IMPORTAR BIBLIOTECAS
#-------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

#-------------------
# CONFIGURAR PÁGINA
#-------------------

# Configuração para tela cheia (modo wide)
st.set_page_config(layout="wide", page_title="Resultados Preliminares SPAECE", page_icon="spaece.png")
st.info("Para melhor visualização, recomendamos usar o tema claro. Você pode alterar o tema nas configurações do Streamlit (Menu (⋮) > Settings > Theme).")

# Adicionando Kanit via CSS no Streamlit
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Kanit', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#-------------------
# AUTENTICAÇÃO
#-------------------
#USERS = {"crede01": "0", "aquiraz": "0", "caucaia": "0", "eusebio": "0","guaiuba":"0","itaitinga":"0","maracanau":"0","maranguape":"0","pacatuba":"0"}
USERS = {
    "anace_joaquim": "x3f7h9",
    "anama_tapeba": "p8l2m5",
    "chui": "k4t9y7",
    "ponte": "m1n5z8",
    "direito_aprender": "h2v8j6",
    "indios_tapeba": "q9w6x4",
    "ita_ara": "r3y7m1",
    "jenipapo_kaninde": "n5t4v9",
    "marcelino_matos": "j8k2h5",
    "narcisio_matos": "l5m8y2",
    "amelia_domingos": "t3v9k7",
    "capoeira": "w4y8m2",
    "capuan": "z9x6q3",
    "trilho": "b5n7r4",
    "vila_cacos": "y8j2k5"
}

ESCOLAS = {
    "anace_joaquim": "ESCOLA INDIGENA ANACE JOAQUIM DA ROCHA FRANCO",
    "anama_tapeba": "ESCOLA INDIGENA ANAMA TAPEBA",
    "chui": "ESCOLA INDIGENA CHUI",
    "ponte": "ESCOLA INDIGENA DA PONTE",
    "direito_aprender": "ESCOLA INDIGENA DIREITO DE APRENDER DO POVO ANACE",
    "indios_tapeba": "ESCOLA INDIGENA INDIOS TAPEBA",
    "ita_ara": "ESCOLA INDIGENA ITA-ARA",
    "jenipapo_kaninde": "ESCOLA INDIGENA JENIPAPO KANINDE",
    "marcelino_matos": "ESCOLA INDIGENA MARCELINO ALVES DE MATOS",
    "narcisio_matos": "ESCOLA INDIGENA NARCISIO FERREIRA MATOS",
    "amelia_domingos": "ESCOLA INDIGENA TAPEBA AMELIA DOMINGOS",
    "capoeira": "ESCOLA INDIGENA TAPEBA CAPOEIRA",
    "capuan": "ESCOLA INDIGENA TAPEBA DE CAPUAN",
    "trilho": "ESCOLA INDIGENA TAPEBA DO TRILHO",
    "vila_cacos": "ESCOLA INDIGENA VILA DOS CACOS"
}

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
            st.image("banner.png", use_container_width=True)
    
    st.title("Entre")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if USERS.get(username) == password:
            st.session_state.update({"authenticated": True, "username": username, "escola": ESCOLAS.get(username, "Desconhecido")})
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")
else:
    usuario = st.session_state["username"]
    escola_usuario = st.session_state["escola"]

    st.sidebar.image("spaece.png", width=250)
    
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
            st.image("banner.png", use_container_width=True)

    
    st.markdown('---')
    st.markdown(f"<h3 style='font-family: Kanit; font-size: 20px; font-weight: bold;'>Seja bem-vindo gestor da escola: {escola_usuario}!</h3>", unsafe_allow_html=True)
    
    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 25px; font-weight: normal;'>Baixe aqui os resultados preliminares do SPAECE 2024 organizados por escola, por turma ou por Estudante.</h3>",
        unsafe_allow_html=True
    )

    # Adicionar linha divisória
    st.write("---")
#-------------------
# IMPORTA OS DADOS (df)
#-------------------

    df = pd.read_csv("df_final.csv")
    # st.text('df')
    # st.dataframe(df, height=400, width=1000)
    
#-------------------
# FILTROS ()
#-------------------
    df_filtrado_escola = df[df["ESCOLA"] == escola_usuario]
    # Filtrando etapas
    etapas_disponiveis = ["Todas"] + sorted(df_filtrado_escola["ETAPA"].unique().tolist())
    
    etapa_filtro = st.sidebar.selectbox("Selecione a Etapa", etapas_disponiveis)

    df_filtrado_etapa = df_filtrado_escola if etapa_filtro == "Todas" else df_filtrado_escola[df_filtrado_escola["ETAPA"] == etapa_filtro]
    
    # Filtrando turmas
    turmas_disponiveis = ["Todas"] + sorted(df_filtrado_etapa["TURMA"].unique().tolist())
    turma_filtro = st.sidebar.selectbox("Selecione a Turma", turmas_disponiveis)

    # Filtrando estudantes
    df_filtrado_turma = df_filtrado_escola if turma_filtro == "Todas" else df_filtrado_escola[df_filtrado_escola["TURMA"] == turma_filtro]
    estudantes_disponiveis = ["Todos"] + sorted(df_filtrado_turma["ESTUDANTE"].unique().tolist())
    estudante_filtro = st.sidebar.selectbox("Selecione o Estudante", estudantes_disponiveis)

    # Filtrando componentes curriculares
    componentes_disponiveis = ["Todos"] + sorted(df_filtrado_turma["COMPONENTE CURRICULAR"].unique().tolist())
    componente_filtro = st.sidebar.selectbox("Selecione o Componente Curricular", componentes_disponiveis)

    # Botão para aplicar os filtros
    #if st.sidebar.button("Aplicar Filtros"):
    # Aplicando todos os filtros
    df_final = df[
        ((df["ESCOLA"] == escola_usuario)) &
        ((df["ETAPA"] == etapa_filtro) | (etapa_filtro == "Todas")) &
        ((df["TURMA"] == turma_filtro) | (turma_filtro == "Todas")) &
        ((df["ESTUDANTE"] == estudante_filtro) | (estudante_filtro == "Todos")) &
        ((df["COMPONENTE CURRICULAR"] == componente_filtro) | (componente_filtro == "Todos"))
    ].copy()
    
    st.dataframe(data=df_final,hide_index=True)

    # Converter DataFrame para Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Dados')
        writer.close()  # Certifique-se de fechar o writer antes de ler o conteúdo
        processed_data = output.getvalue()

    # Criar botão para download
    st.download_button(
        label="Baixar Tabela de Dados em Excel",
        data=processed_data,
        file_name='tabela_de_dados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
        
    st.markdown("---")


    
    #RESUMO
    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 20px; font-weight: bold;'>RESUMO</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 18px; font-weight: bold;'>Média das proficiências dos alunos presentes:</h3>",
        unsafe_allow_html=True
    )
    
    # Filtrar apenas os estudantes avaliados
    df_avaliados = df_final[df_final['AVALIADO'] == 'SIM']
    
    # Remover duplicatas de estudantes para considerar apenas um registro por estudante
    df_unicos = df_avaliados.drop_duplicates(subset=['ESTUDANTE'])
    
    # Calcular a média das proficiências
    media_proficiencia = round(df_unicos['PROFICIENCIA MÉDIA'].astype(float).mean(),0)

    st.metric(label="Proficiência Média", value=media_proficiencia)
    
    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 18px; font-weight: bold;'>Frequência:</h3>",
        unsafe_allow_html=True
    )

    avaliados = df_final[df_final['AVALIADO'] == 'SIM']['ESTUDANTE'].nunique()
    n_avaliados = df_final[df_final['AVALIADO'] == 'NÃO']['ESTUDANTE'].nunique()
    
    # Criar três colunas
    col1, col2, col3 = st.columns(3)

    # Exibir os dados nas colunas
    col1.metric(label="Total de Estudantes", value=avaliados+n_avaliados)
    col2.metric(label="Avaliados", value=avaliados)
    col3.metric(label="Não Avaliados", value=n_avaliados)

    # Definir a ordem desejada das faixas
    ordem_faixas = [
        "MUITO CRÍTICO", "CRÍTICO", "BÁSICO", "SUFICIENTE", 
        "INTERMEDIÁRIO", "ADEQUADO", "DESEJÁVEL", "PROFICIENTE", "AVANÇADO"
    ]

    # Definir cores personalizadas para cada faixa
    cores_faixas = {
        "MUITO CRÍTICO": "#D32F2F",   # Vermelho escuro
        "CRÍTICO": "#F44336",         # Vermelho
        "BÁSICO": "#FF9800",          # Laranja
        "SUFICIENTE": "#FFEB3B",      # Amarelo
        "INTERMEDIÁRIO": "#4CAF50",   # Verde médio
        "ADEQUADO": "#388E3C",        # Verde escuro
        "DESEJÁVEL": "#2196F3",       # Azul
        "PROFICIENTE": "#3F51B5",     # Azul escuro
        "AVANÇADO": "#673AB7"         # Roxo
    }
    
    # Contar a quantidade de estudantes únicos para cada faixa (somente os avaliados "SIM")
    faixa_counts = df_final[df_final['AVALIADO'] == 'SIM'].groupby('FAIXAS')['ESTUDANTE'].nunique()
    
    # Reorganizar os dados conforme a ordem desejada, removendo faixas com valor 0
    faixa_counts = {faixa: faixa_counts.get(faixa, 0) for faixa in ordem_faixas}
    faixa_counts = {faixa: count for faixa, count in faixa_counts.items() if count > 0}  # Remove os zeros
    
    
    # Criar colunas dinamicamente com as faixas filtradas
    cols = st.columns(len(faixa_counts))
    
    # Exibir cada faixa na ordem definida
    #for col, (faixa, count) in zip(cols, faixa_counts.items()):
    #    col.metric(label=faixa, value=count)

    # Criar DataFrame para o gráfico
    df_faixas = pd.DataFrame(list(faixa_counts.items()), columns=["Faixa", "Quantidade"])
    
    # Criar gráfico de barras
    fig = px.bar(df_faixas, x="Faixa", y="Quantidade", text="Quantidade",
                 title="Distribuição de Estudantes por Faixa",
                 labels={"Faixa": "Faixa de Proficiência", "Quantidade": "Número de Estudantes"},
                 color="Faixa",
                 color_discrete_map=cores_faixas) # Adiciona cores diferentes para cada faixa
    
    fig.update_traces(textposition="outside")  # Exibir valores fora das barras

    st.plotly_chart(fig)

    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()
