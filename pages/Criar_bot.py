import streamlit as st
from functions.utils_chatbot import check_unique_telegram_key, save_new_chatbot, generate_chatbot_version, upload_chatbot_version
from streamlit_extras.switch_page_button import switch_page
from functions.utils import get_decrypted_cookie, show_logout

# st.set_page_config(
#     page_title="Novo chatbot",
#     page_icon="🤖"
# )

print("\n\n\nEntrou criar bot\n\n\n")
st.empty()

def create_bot_widget():
    st.title("Criar bot")

    # Campo para o nome do bot
    chatbot_name = st.text_input("Nome do Bot")

    # Campo para a API KEY do Telegram
    api_key_telegram = st.text_input("API KEY Telegram", help="Obtenha a API KEY no site de documentação.")
    check_unique_telegram_key(api_key_telegram)
    
    # Campo de descrição do bot (text area)
    chatbot_description = st.text_area("Descrição")

    st.divider() 
    st.subheader("Configurações")


    # Campo para a URL de início
    start_url = st.text_input("URL de Início")

    # Campo para domínios permitidos (lista de strings)
    allowed_domains = st.text_input("Domínios Permitidos (separados por vírgula)")

    # Campo para tipos de arquivos permitidos (lista de strings)
    allowed_files = st.text_input("Tipos de Arquivos Permitidos (separados por vírgula)")
    
    content_element = st.text_input("Elemento HTML onde o conteúdo é exibido", placeholder="Ex: #Content")


    st.divider() 
    st.subheader("Personalização avançada")

    # Campo para o limite de profundidade
    depth_limit = st.number_input("Limite de Profundidade", value=2, min_value=0, max_value=10)

    # Campo para o número máximo de requisições assíncronas
    max_assync_requests = st.number_input("Máximo de Requisições Assíncronas", value=8, min_value=0, max_value=20)

    # Campo para o atraso nas requisições (em milissegundos)
    requests_delay_seg = st.number_input("Atraso nas Requisições (em segundos)", value=0.5, min_value=0.0, max_value=100.0)


    # Botões para Salvar, Limpar e Cancelar
    if st.button("Salvar"):
        version_id = '1.0'
        chatbot_id = save_new_chatbot(chatbot_name, api_key_telegram, chatbot_description, start_url, allowed_domains, allowed_files, content_element, requests_delay_seg, max_assync_requests, depth_limit, userId, version_id)
        if chatbot_id:
            
            st.success(f"Bot '{chatbot_name}' salvo com sucesso!")
            generate_chatbot_version(chatbot_id,version_id)
        
            
            
        else:
            st.error("Erro ao criar o novo bot!")
        
        
userId = None

if 'LOGGED_IN' in st.session_state and st.session_state['LOGGED_IN'] == True:
    
        userId = get_decrypted_cookie("__userId__")
        show_logout()
        create_bot_widget()

else:
    switch_page("login")

