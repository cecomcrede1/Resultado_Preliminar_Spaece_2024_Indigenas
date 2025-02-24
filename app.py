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
    escola_filtro = df[df["ESCOLA"] == escola_usuario]
 
    # Filtrando turmas
    df_filtrado_escola = escola_filtro
    turmas_disponiveis = ["Todas"] + sorted(df_filtrado_escola["TURMA"].unique().tolist())
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
    # Criar um dicionário para armazenar os resultados de cada componente curricular
    resultados_por_componente = {}
    
    # Processar cada DataFrame de componente curricular
    for componente in ['LP','MT']:
        # Calcular quantidade de alunos e média de proficiência
        resumo = df_componente.agg(
            quantidade_alunos=("ESTUDANTE", "count"),
            media_proficiencia=("PROFICIENCIA MÉDIA", "mean")
        ).to_frame().T
    
        # Contar a quantidade de alunos por faixa
        faixas_counts = df_componente["FAIXAS"].value_counts().to_frame().T
    
        # Adicionar o nome do componente curricular
        resumo["COMPONENTE CURRICULAR"] = componente
    
        # Unir as informações
        resultado_final = resumo.merge(faixas_counts, left_index=True, right_index=True, how="left")
    
        # Armazenar no dicionário
        resultados_por_componente[componente] = resultado_final
    
    # Concatenar todos os resultados em um único DataFrame
    df_resultados_finais = pd.concat(resultados_por_componente.values(), ignore_index=True)

    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()
