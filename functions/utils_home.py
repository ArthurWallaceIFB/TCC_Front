import pymongo
import streamlit as st
from Scraping.Scraping import run_scrapy_chatbot_version
from datetime import datetime
from bson import ObjectId
from functions.utils_chatbot import generate_chatbot_version
import requests

@st.cache_resource
def init_connection():
    client = pymongo.MongoClient(st.secrets["mongo"]["url"])
    db = client.TCC
    return db
db = init_connection()

api_url = st.secrets["API_URL"]
print(api_url)

chatbots_collection = db.chatbots
versions_collection = db.chatbot_versions

def get_user_chatbots(user_id):
    try:
        user_chatbots = chatbots_collection.find({"UserIds": user_id})
        user_list = list(user_chatbots)
        
         # Para cada chatbot do usuário, busca as versões e adiciona ao campo "versions"
        for chatbot in user_list:
            chatbot_id = ObjectId(chatbot["_id"])
            versions = list(versions_collection.find({"chatbot_id": chatbot_id}, {"_id": 1, "chatbot_id": 1, "version_id": 1, "created_at": 1}).sort("created_at", pymongo.DESCENDING))
            chatbot["versions"] = versions
        
        return user_list
    
    except Exception as e:
        print(f"Erro ao buscar chatbots do usuário no MongoDB: {e}")
        return None
    

def activate_bot_id(bot_id):
    try:
        request_url = f"{api_url}/iniciar_bot" # Substitua pela URL correta da sua API
        payload = {"chatbot_id": str(bot_id)}
        response = requests.post(request_url, json=payload)
        if response.status_code == 200:
            #st.success("Versão adicionada com sucesso!")
            return True
        else:
            raise Exception(response.json())
            return False
    
    except Exception as e:
        st.error(f"Erro ao desativar o bot: {e}")
        return False
    
def disable_bot_id(bot_id):
    try:
        request_url = f"{api_url}/encerrar_bot" # Substitua pela URL correta da sua API
        payload = {"chatbot_id": str(bot_id)}
        response = requests.post(request_url, json=payload)
        if response.status_code == 200:
            #st.success("Versão adicionada com sucesso!")
            return True
        elif response.status_code == 500 and response.json()['message'] == "Bot não encontrado com este token":
            return True
        else:
            raise Exception(response.json())
            return False
    
    except Exception as e:
        st.error(f"Erro ao desativar o bot: {e}")
        return False


def delete_bot_id(bot_id):
    try:
        
        if disable_bot_id(str(bot_id)):
            # Obtém todas as versões associadas ao bot
            versions = versions_collection.find({"chatbot_id": bot_id})
            
            # Remove todas as versões associadas ao bot
            for version in versions:
                versions_collection.delete_one({"_id": version["_id"]})
                
            result = chatbots_collection.delete_one({"_id": bot_id})
            
            if result.deleted_count == 1:
                # Se um documento foi removido, desative o bot na API
                return True
            else:
                return False
    
    except Exception as e:
        st.error(f"Erro ao deletar o bot: {e}")
        return False
    
    
def get_running_bots():
    try:
        request_url = f"{api_url}/listar_processos" # Substitua pela URL correta da sua API
        response = requests.get(request_url)
        if response.status_code == 200:
            #st.success("Versão adicionada com sucesso!")
            return response.json()
        else:
            raise Exception(response.json())
    
    except Exception as e:
        raise Exception(e)
    
def activate_version_by_id(version_id_db):
    try:
        # Encontrar a versão pelo ID
        version = versions_collection.find_one({"_id": version_id_db})
        
        if version:
            # Atualizar o campo 'actual_version' na collection de chatbots
            chatbots_collection.update_one({"_id": version["chatbot_id"]}, {"$set": {"active_version": version["version_id"]}})
            #st.success(f"Versão ativada com sucesso para o Chatbot de ID: {version['chatbot_id']}")
            
            request_url = f"{api_url}/atualizar_bot" # Substitua pela URL correta da sua API
            payload = {"chatbot_id": str(version["chatbot_id"])}
            response = requests.post(request_url, json=payload)
            if response.status_code == 200:
                # A request foi bem-sucedida
                return True
            else:
                raise Exception(response.json())
                return False
            
            return True
        else:
            #st.warning(f"Versão com ID {version_id_db} não encontrada.")
            return False
    
    except Exception as e:
        print("Erro: ", e)
        st.error(f"Erro ao ativar a versão: {e}")
        return False


def delete_version_by_id(version_id_db):
    try:
        # Encontrar a versão pelo ID
        version = versions_collection.find_one({"_id": version_id_db})
        
        if version:
            # Excluir a versão da collection de versões
            versions_collection.delete_one({"_id": version_id_db})
            
            return True
        else:
            st.warning(f"Versão com ID {version_id_db} não encontrada.")
            return False
    
    except Exception as e:
        st.error(f"Erro ao excluir a versão no MongoDB: {e}")
        return False
    

def update_chatbot_version(chatbot_id):
    try:
        # Buscar as versões do bot ordenadas por ordem decrescente pela data de criação
        versions = list(versions_collection.find({"chatbot_id": ObjectId(chatbot_id)}, {"_id": 1, "version_id": 1, "created_at": 1}).sort("created_at", pymongo.DESCENDING))

        if versions:
            # Obter o número da última versão e incrementar 1
            last_version_number = int(versions[0]["version_id"].split(".")[0])
            new_version_number = f"{last_version_number + 1}.0"

            # Chamar a função para gerar a nova versão
            generate_chatbot_version(ObjectId(chatbot_id), new_version_number)
            
            return True
            
        else:
            st.warning(f"Nenhuma versão encontrada para o Chatbot de ID: {chatbot_id}")
            return False

    except Exception as e:
        print("Erro: ", e)
        st.error(f"Erro ao atualizar a versão do chatbot no MongoDB: {e}")
        return False