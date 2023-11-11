import streamlit as st
import json
from streamlit_extras.switch_page_button import switch_page
import time
from datetime import datetime

st.set_page_config(
    page_title="Home - IFBots",
    page_icon="🤖"
)

if 'LOGGED_IN' in st.session_state and st.session_state['LOGGED_IN'] == True:
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Carregando os dados do arquivo JSON
    with open('chatbot_data.json', 'r') as json_file:
        dados = json.load(json_file)

    st.title("Gestão de Chatbots 🤖")

    st.write(datetime.now())

    st.markdown('<span id="button-after-create-bot"></span>', unsafe_allow_html=True)
    # Botão para criar um novo chatbot
    if st.button("Criar Novo Chatbot",  key='botao_novo_chatbot'):
        switch_page("Criar bot")
        pass

    # Menu suspenso para selecionar um chatbot
    selected_chatbot = st.selectbox("Selecione um chatbot", [bot['chatbot_name'] for bot in dados])

    def atualizar_versao():
        with st.spinner('Atualizando versão...'):
            time.sleep(5)
        st.success('Atualização concluída!')
        
    def ativar_versao(id):
        with st.spinner(f'Ativando versão {id}...'):
            time.sleep(5)
        st.success(f'Versão {id} ativada com sucesso!')

    # Função para exibir o status (emoji 🟢 ao lado do texto quando o status é ativo)
    def exibir_status(status, id):
        if status == "Ativo":
            container.markdown('<span id="button-after-update-version"></span>', unsafe_allow_html=True)
            if container.button("Atualizar", key="atualizar"):
                atualizar_versao()
                
            return "Ativo 🟢"
        else:
            container.markdown('<span id="button-after-activate-version"></span>', unsafe_allow_html=True)
            if container.button("Ativar"):
                ativar_versao(id)
            return "Inativo"

    # Mostrar versões do chatbot selecionado
    for bot in dados:
        if bot['chatbot_name'] == selected_chatbot:
            st.subheader(f"**Chatbot: {bot['chatbot_name']}**")
            st.write(f"**Data de criação:** {bot['creation_date']}")
            

            for versao in bot['versions']:
                container = st.container()
                container.markdown('#### Versão: {0}'.format(versao['id']), unsafe_allow_html=True)
                is_active = versao['id'] == bot['active_version']
                container.write("**Status:** " + exibir_status("Ativo" if is_active else "Inativo", id=versao['id']))
                container.write(f"**URLs:** {', '.join(versao['Urls'])}")
                container.write(f"**Data de atualização:** {versao['UpdatedAt']}")

else:
    print("Erro")

