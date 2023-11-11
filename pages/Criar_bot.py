import streamlit as st
from functions.utils_create_bot import check_unique_telegram_key, save_new_chatbot, generate_chatbot_version, upload_chatbot_version
import streamlit as st

# st.set_page_config(
#     page_title="Novo chatbot",
#     page_icon="🤖"
# )



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
        chatbot_id = save_new_chatbot(chatbot_name, api_key_telegram, chatbot_description, start_url, allowed_domains, allowed_files, content_element, requests_delay_seg, max_assync_requests, depth_limit)
        version_id = '1.0'
        if chatbot_id:
            
            st.success(f"Bot '{chatbot_name}' salvo com sucesso!")
            with st.spinner(f'Gerando a versão {version_id} do chatbot...'):
                return_generate = generate_chatbot_version(chatbot_id,version_id)
            if return_generate["success"] == True:    
                st.success(return_generate["msg"])
                
                with st.spinner(f'Salvando os dados da versão {version_id} no banco...'):
                    return_upload_version = upload_chatbot_version(chatbot_id,version_id, return_generate["file_path"])
                st.success("Salvo com sucesso!")
            else:
                st.error(return_generate["msg"])
            
            
        else:
            st.error("Erro ao criar o novo bot!")
        
        
        
# st.title("Executar Spider Scrapy a partir do Streamlit")

# start_button = st.button("Iniciar Spider Scrapy")


# if start_button:
#     st.write("Iniciando o Spider Scrapy...")
#     start_urls = [
#         "https://www.ifb.edu.br/espaco-do-estudante/estagio/boletins-de-estagio/36579-boletim-de-estagio-n-40-2013-vagas-de-30-10-a-3-11"
#     ]
#     depth_limit = 2
#     download_delay = 0.5
#     accepted_files = ["pdf"]
#     allowed_domains = ["www.ifb.edu.br", "ifb.edu.br", "processoseletivo.ifb.edu.br"]
#     content_element = "#content"

#     run_scrapy_chatbot_version(start_urls, depth_limit, download_delay, accepted_files, content_element, allowed_domains, content_element, "teste_salvar.json")
#     #reactor.run()  # o script irá bloquear aqui até que o crawling esteja concluído
#     st.write("Spider Scrapy concluído!")

create_bot_widget()

