import pymongo
import streamlit as st
from Scraping.Scraping import run_scrapy_chatbot_version
from datetime import datetime
from bson import ObjectId
from functions.utils_chatbot import generate_chatbot_version

@st.cache_resource
def init_connection():
    client = pymongo.MongoClient(st.secrets["mongo"]["url"])
    db = client.TCC
    return db
db = init_connection()

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
    
def activate_version_by_id(version_id_db):
    try:
        # Encontrar a versão pelo ID
        version = versions_collection.find_one({"_id": version_id_db})
        
        if version:
            # Atualizar o campo 'actual_version' na collection de chatbots
            chatbots_collection.update_one({"_id": version["chatbot_id"]}, {"$set": {"active_version": version["version_id"]}})
            #st.success(f"Versão ativada com sucesso para o Chatbot de ID: {version['chatbot_id']}")
            
            
            #TODO ADICIONAR REQUEST API PARA BUSCAR NOVAMENTE A VERSÃO NO MONGO
            
            return True
        else:
            #st.warning(f"Versão com ID {version_id_db} não encontrada.")
            return False
    
    except Exception as e:
        #st.error(f"Erro ao ativar a versão no MongoDB: {e}")
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
        st.error(f"Erro ao atualizar a versão do chatbot no MongoDB: {e}")
        return False