import pymongo
import streamlit as st
from Scraping.Scraping import run_scrapy_chatbot_version
from datetime import datetime


@st.cache_resource
def init_connection():
    client = pymongo.MongoClient(st.secrets["mongo"]["url"])
    db = client.TCC
    return db

db = init_connection()

chatbots_collection = db.chatbots
versions_collection = db.chatbot_versions


def check_unique_telegram_key(telegram_key: str) -> bool:
    return True


def save_new_chatbot(
    chatbot_name,
    telegram_api_key,
    chatbot_description,
    start_url,
    allowed_domains,
    allowed_files,
    content_element,
    requests_delay_ms,
    max_assync_requests,
    depth_limit,
    user_id,
    version_id
):
    try:
        # Monte o objeto do novo bot
        bot_data = {
            "chatbot_name": chatbot_name,
            "UserIds": [user_id],
            "telegram_api_key": telegram_api_key,
            "chatbot_description": chatbot_description,
            "start_url": start_url,
            "allowed_domains": allowed_domains.split(","),
            "allowed_files": allowed_files.split(","),
            "download_delay": requests_delay_ms,
            "max_assync_requests": max_assync_requests,
            "depth_limit": depth_limit,
            "content_element": content_element,
            "active_version": version_id
        }

        # Insira os dados do novo bot na coleção
        inserted_data = chatbots_collection.insert_one(bot_data)
        inserted_id = inserted_data.inserted_id
        return inserted_id  # Retorna o ID do documento inserido
    except Exception as e:
        print(f"Erro ao salvar o bot no MongoDB: {e}")
        return None  # Retorne None em caso de erro na inserção


def get_chatbot_info(bot_id):
    try:
        print(bot_id)
        chatbot_info = chatbots_collection.find_one({"_id": bot_id})

        return chatbot_info
    except Exception as e:
        print(f"Erro ao buscar informações do chatbot no MongoDB: {e}")
        return None


def generate_chatbot_version(bot_id, version_name):
    # Busque as informações do chatbot no MongoDB
    chatbot_info = get_chatbot_info(bot_id)
    chatbot_name = chatbot_info.get("chatbot_name")
    if chatbot_info:
        start_urls = [chatbot_info.get("start_url")]
        accepted_files = chatbot_info.get("allowed_files")
        allowed_domains = chatbot_info.get("allowed_domains")
        depth_limit = chatbot_info.get("depth_limit")
        download_delay = chatbot_info.get("download_delay")
        content_element = chatbot_info.get("content_element")
        output_filename = f"chatbot_{bot_id}_version_{version_name}.json"

        run_scrapy_chatbot_version(
            start_urls,
            depth_limit,
            download_delay,
            accepted_files,
            allowed_domains,
            content_element,
            output_filename,
        )

        return {
            "success": True,
            "msg": f"Versão '{version_name}' do chatbot '{chatbot_name}' gerada com sucesso!",
            "file_path": output_filename
        }
    else:
        return {
            "success": False,
            "msg": "Erro ao buscar informações do chatbot no banco de dados!"
        }


def upload_chatbot_version(chatbot_id,version_id, file_path):
    # Ler o conteúdo do arquivo
    with open(file_path, "r") as file:
        content = file.read()

    # Criar a estrutura de dados
    data = {
        "chatbot_id": chatbot_id,
        "version_id": version_id,
        "created_at": datetime.now(),
        "content": content,
    }

    # Inserir os dados na coleção
    result = versions_collection.insert_one(data)

    # Verificar se a inserção foi bem-sucedida
    if result.inserted_id:
        print(f"Versão {version_id} do Chatbot {chatbot_id} foi enviada com sucesso.")
    else:
        print("Erro ao enviar a versão do Chatbot.")
