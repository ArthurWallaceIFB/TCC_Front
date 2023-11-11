import pymongo
import streamlit as st
from Scraping.Scraping import run_scrapy_chatbot_version
from datetime import datetime
import functions.utils_chatbot
from bson import ObjectId

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
            versions = list(versions_collection.find({"chatbot_id": chatbot_id}, {"_id": 1, "chatbot_id": 1, "version_id": 1, "created_at": 1}))
            chatbot["versions"] = versions
        
        return user_list
    
    except Exception as e:
        print(f"Erro ao buscar chatbots do usuário no MongoDB: {e}")
        return None