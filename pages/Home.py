import streamlit as st
import json
from streamlit_extras.switch_page_button import switch_page
import time
from datetime import datetime
from functions.utils_home import get_user_chatbots
from functions.utils import get_decrypted_cookie, show_logout
from pages.Criar_bot import userId

# st.set_page_config(
#     page_title="Home - IFBots",
#     page_icon="🤖"
# )   

def Home_widget():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    dados = get_user_chatbots(userId)
    
    # Carregando os dados do arquivo JSON
    # with open('chatbot_data.json', 'r') as json_file:
    #     dados = json.load(json_file)

    st.title("Gestão de Chatbots 🤖")


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
    def exibir_status(status, version_id, bot_id):
        if status == "Ativo":
            container.markdown('<span id="button-after-update-version"></span>', unsafe_allow_html=True)
            button_key = f"atualizar_{bot_id}_{version_id}"
            if container.button("Atualizar", key=button_key):
                atualizar_versao()
                
            return "Ativo 🟢"
        else:
            container.markdown('<span id="button-after-activate-version"></span>', unsafe_allow_html=True)
            if container.button("Ativar"):
                ativar_versao(version_id)
            return "Inativo"

    # Mostrar versões do chatbot selecionado
    for bot in dados:
        if bot['chatbot_name'] == selected_chatbot:
            st.subheader(f"**Chatbot: {bot['chatbot_name']}**")
            if bot.get('creation_date'):
                st.write(f"**Data de criação:** {bot['creation_date']}")
            

            if bot.get('versions'):
                for versao in bot['versions']:
                    container = st.container()
                    container.markdown('#### Versão: {0}'.format(versao['version_id']), unsafe_allow_html=True)
                    is_active = versao['version_id'] == bot['active_version']
                    container.write("**Status:** " + exibir_status("Ativo" if is_active else "Inativo", version_id=versao['version_id'], bot_id=versao['chatbot_id']))
                    #container.write(f"**URLs:** {', '.join(versao['Urls'])}")
                    container.write(f"**Data de criação:** {versao['created_at']}")



userId = None

if 'LOGGED_IN' in st.session_state and st.session_state['LOGGED_IN'] == True:
    
        userId = get_decrypted_cookie("__userId__")
        show_logout()                
        Home_widget()
        
else:
    print("Not logged")
    switch_page("login")

