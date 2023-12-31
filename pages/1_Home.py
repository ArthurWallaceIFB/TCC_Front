import streamlit as st

st.set_page_config(
    page_title="Home - IFBots",
    page_icon="🤖"
)   

import json
from streamlit_extras.switch_page_button import switch_page
import time
from datetime import datetime
from functions.utils_home import (activate_bot_id, activate_version_by_id, delete_version_by_id,
    disable_bot_id, get_running_bots, get_user_chatbots, update_chatbot_version, delete_bot_id)
from functions.utils import get_decrypted_cookie, show_logout


st.empty()

def Home_widget():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    with st.spinner(f'Buscando os dados do usuário...'):
        dados = get_user_chatbots(userId)
    if dados is None:
        st.error("Erro ao buscar os dados do usuário!")
        st.stop()
    
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

    def atualizar_versao(bot_id):
        update_chatbot_version_return = update_chatbot_version(bot_id)
        if update_chatbot_version_return == True:
            time.sleep(0.3)
            st.rerun()
        
    def ativar_versao(version_name, version_id_db):
        with st.spinner(f'Ativando versão {version_name}...'):
            activate_version_return = activate_version_by_id(version_id_db)
            if activate_version_return == True:
                st.success(f'Versão {version_name} ativada com sucesso!')
                time.sleep(0.3)
                st.rerun()
            else:
                st.error(f"Erro ao ativar versão {version_name}")
    
    def deletar_versao(version_name, version_id_db):
        with st.spinner(f'Deletando versão {version_name}...'):
            delete_version_return = delete_version_by_id(version_id_db)
            if delete_version_return == True:
                st.success(f"Versão {version_name} deletada com sucesso!")
                time.sleep(0.3)
                st.rerun()
    
    def ativar_bot(bot_id):
        with st.spinner(f'Ativando o chatbot no Telegram...'):
            activate_bot_return = activate_bot_id(bot_id)
            if activate_bot_return == True:
                st.success(f'Chatbot ativado com sucesso!')
                time.sleep(0.3)
                st.rerun()
            else:
                st.error(f"Erro ao ativar o chatbot!")
    
    def desativar_bot(bot_id):
        with st.spinner(f'Desativando o chatbot...'):
            disable_bot_return = disable_bot_id(bot_id)
            if disable_bot_return == True:
                st.success(f"Chatbot desativado com sucesso!")
                time.sleep(0.3)
                st.rerun()
            else:
                 st.error(f"Erro ao desativar o chatbot!")
    
    def deletar_bot(bot_id):
        with st.spinner(f'Deletando o chatbot...'):
            delete_bot_return = delete_bot_id(bot_id)
            if delete_bot_return == True:
                st.success(f"Chatbot deletado com sucesso!")
                time.sleep(0.3)
                st.rerun()
            else:
                st.error(f"Erro ao deletar o chatbot!")
        


    # Função para exibir o status (emoji 🟢 ao lado do texto quando o status é ativo)
    def exibir_status(status, version_name, bot_id, version_id_db):
        if status == "Ativo":
            container.markdown('<span id="button-after-update-version"></span>', unsafe_allow_html=True)
            button_key = f"atualizar_{bot_id}_{version_name}"
            if container.button("Atualizar", key=button_key):
                atualizar_versao(bot_id)
                
            return "Ativa 🟢"
        else:
            container.markdown('<span id="button-after-activate-version"></span>', unsafe_allow_html=True)
            button_key = f"ativar_{bot_id}_{version_name}"
            if container.button("Ativar", key=button_key):
                ativar_versao(version_name, version_id_db)
            
            container.markdown('<span id="button-after-delete-version"></span>', unsafe_allow_html=True)
            delete_button_key = f"deletar_{bot_id}_{version_name}"
            if container.button("🗑️", key=delete_button_key):
                deletar_versao(version_name, version_id_db)
            return "Inativa"

    # Mostrar versões do chatbot selecionado
    for bot in dados:
        if bot['chatbot_name'] == selected_chatbot:
            st.subheader(f"**Chatbot: {bot['chatbot_name']}**")
            with st.expander("Detalhes do bot"):
                if bot.get('creation_date'):
                    st.write(f"**Data de criação:** {datetime.strptime(str(bot['creation_date']), '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M:%S')}")
                st.write(f"**Versão Ativa:** {bot['active_version']}")
                st.write(f"**URL Inicial:** {bot['start_url']}")
                st.write(f"**Domínios permitidos:** {', '.join(bot['allowed_domains'])}")
                st.write(f"**Arquivos permitidos:** {', '.join(bot['allowed_files'])}")
                st.divider()
                st.subheader("Configurações Avançadas")
                st.write(f"**Profundidade de busca:** {bot['depth_limit']}")
                st.write(f"**Delay entre requisições:** {bot['download_delay']}s")
                st.write(f"**Máximo de requisições Assync:** {bot['max_assync_requests']}")
                st.write(f"**Elemento HTML de conteúdo:** {bot['content_element']}")
                if st.button("Deletar bot"):
                    deletar_bot(bot['_id'])
            try:
                running_bots = get_running_bots()
                #print(running_bots)
                if bot['telegram_api_key'] in running_bots['processes']:
                    st.subheader(f"Status do Chatbot no Telegram: **:green[{'Ativo'}]**")
                    st.write(f"**URL do bot:** {bot['telegram_bot_url']}")
                    st.markdown('<span id="button-after-disable-chatbot"></span>', unsafe_allow_html=True)
                    button_key = f"desativar_{bot['_id']}"
                    if st.button("Desativar", key=button_key):
                        desativar_bot(bot['_id'])
                else:
                    st.subheader(f"Status do Chatbot no Telegram: **:red[{'Desativado'}]**")
                    st.markdown('<span id="button-after-activate-chatbot"></span>', unsafe_allow_html=True)
                    button_key = f"ativar_{bot['_id']}"
                    if st.button("Ativar", key=button_key):
                        ativar_bot(bot['_id'])
                        
            except Exception as e:
                st.error(f"Erro ao buscar os bots em execução! Verifique a disponibilidade do servidor: {e}")
                st.stop()
            

            if bot.get('versions'):
                st.divider()
                for versao in bot['versions']:
                    container = st.container()
                    container.markdown('#### Versão: {0}'.format(versao['version_id']), unsafe_allow_html=True)
                    is_active = versao['version_id'] == bot['active_version']
                    container.write("**Status:** " + exibir_status("Ativo" if is_active else "Inativo", version_name=versao['version_id'], bot_id=versao['chatbot_id'], version_id_db=versao['_id']))
                    #container.write(f"**URLs:** {', '.join(versao['Urls'])}")
                    container.write(f"**Data de criação:** {datetime.strptime(str(versao['created_at']), '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M:%S')}")



userId = None

if 'LOGGED_IN' in st.session_state and st.session_state['LOGGED_IN'] == True:
    
        userId = get_decrypted_cookie("__userId__")
        show_logout()                
        Home_widget()
        
else:
    print("\n\nNot logged HOME\n\n")
    switch_page("login")

