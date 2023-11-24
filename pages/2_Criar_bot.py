import streamlit as st

st.set_page_config(
    page_title="Novo chatbot",
    page_icon="🤖"
)

from functions.utils_chatbot import (
    validate_telegram_api_key,
    check_unique_telegram_key,
    save_new_chatbot,
    generate_chatbot_version,
    upload_chatbot_version,
)
from streamlit_extras.switch_page_button import switch_page
from functions.utils import get_decrypted_cookie, show_logout
from streamlit_tags import st_tags


st.empty()


def create_bot_widget():
    st.title("Criar Novo Chatbot")

    # Campo para o nome do bot
    chatbot_name = st.text_input("Nome do Chatbot :red[*]")

    # Campo para a URL do Telegram
    telegram_bot_url = st.text_input(
        "URL do Telegram :red[*]", help="A URL em que seu bot se encontra em execução no Telegram."
    )
    
    # Campo para a API KEY do Telegram
    api_key_telegram = st.text_input(
        "API KEY do Telegram :red[*]", help="Obtenha a API KEY no site de documentação: https://core.telegram.org/bots/features#creating-a-new-bot."
    )
    if api_key_telegram:
        valid_telegram_key = validate_telegram_api_key(api_key_telegram)
        if(valid_telegram_key is False):
            st.error("Digite um token válido para a API do Telegram!")
            
        unique_telegram_key = check_unique_telegram_key(api_key_telegram)
        print(unique_telegram_key)
        if(unique_telegram_key is False):
                st.error("Essa API key já está em uso!")
            
    # Campo de descrição do bot (text area)
    initial_message = st.text_area(
        "Mensagem de boas-vindas :red[*]",
        placeholder="Digite a mensagem de boas vindas que será apresentada na 1ª interação do usuário!",
    )

    st.divider()
    st.subheader("Configurações")

    # Campo para a URL de início
    start_url = st.text_input("URL de Início :red[*]")

    # Campo para domínios permitidos (lista de strings)
    #allowed_domains = st.text_input("Domínios Permitidos (separados por vírgula) :red[*]")
    
    allowed_domains = st_tags(label='Domínios permitidos :red[*]', text='Digite o domínio e pressione ENTER')

    # Campo para tipos de arquivos permitidos (lista de strings)
    # allowed_files = st.text_input("Tipos de Arquivos Permitidos (separados por vírgula)")
    allowed_files_pdf = st.checkbox("Permitir arquivos PDF")

    if allowed_files_pdf:
        allowed_files = "pdf"
    else:
        allowed_files = ""

    content_element = st.text_input(
        "Elemento HTML onde o conteúdo é exibido", placeholder="Ex: #content"
    )

    st.divider()
    st.subheader("Personalização Avançada")

    # Campo para o limite de profundidade
    depth_limit = st.number_input(
        "Limite de Profundidade", value=2, min_value=0, max_value=10
    )

    # Campo para o número máximo de requisições assíncronas
    max_assync_requests = st.number_input(
        "Máximo de Requisições Assíncronas", value=8, min_value=0, max_value=20
    )

    # Campo para o atraso nas requisições (em milissegundos)
    requests_delay_seg = st.number_input(
        "Atraso nas Requisições (em segundos)",
        value=0.5,
        min_value=0.0,
        max_value=100.0,
    )

    # Botões para Salvar, Limpar e Cancelar
    if st.button("Salvar"):
        # Verifica se os campos obrigatórios estão preenchidos
        if not chatbot_name or not telegram_bot_url or not api_key_telegram or not initial_message or not start_url or not allowed_domains:
            st.error("Preencha todos os campos obrigatórios (*) antes de salvar.")
        else:
            # Restante do código para salvar o bot
            version_id = "1.0"
            chatbot_id = save_new_chatbot(
                chatbot_name,
                telegram_bot_url,
                api_key_telegram,
                initial_message,
                start_url,
                allowed_domains,
                allowed_files,
                content_element,
                requests_delay_seg,
                max_assync_requests,
                depth_limit,
                userId,
                version_id,
            )
            if chatbot_id:
                st.success(f"Bot '{chatbot_name}' salvo com sucesso!")
                generate_chatbot_version(chatbot_id, version_id)
            else:
                st.error("Erro ao criar o novo bot!")


userId = None

if "LOGGED_IN" in st.session_state and st.session_state["LOGGED_IN"] == True:
    userId = get_decrypted_cookie("__userId__")
    show_logout()
    create_bot_widget()

else:
    switch_page("login")
