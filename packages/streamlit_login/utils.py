import re
import json
from trycourier import Courier
import secrets
from argon2 import PasswordHasher
import requests
import pymongo
import streamlit as st


@st.cache_resource
def init_connection():
    client = pymongo.MongoClient(st.secrets["mongo"]["url"])
    db = client.TCC
    return db.users

collection = init_connection()


ph = PasswordHasher() 

def check_usr_pass(username: str, password: str):
    """
    Authenticates the username and password.
    """
    user = collection.find_one({"username": username})
    if user:
        try:
            if ph.verify(user['password'], password):
                return {"success": True, "userId": str(user['_id'])}
        except Exception as e:
            pass
    return {"success": False}


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    user = collection.find_one({"email": email_sign_up})
    return not user

def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    
    user = collection.find_one({"username": username_sign_up})
    
    if user:
        return False
    
    non_empty_check = non_empty_str_check(username_sign_up)
    
    if not non_empty_check:
        return None
    return True


def register_new_usr(name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
    """
    Saves the information of the new user in the _secret_auth.json file.
    """

    new_usr_data = {
        'username': username_sign_up,
        'name': name_sign_up,
        'email': email_sign_up,
        'password': ph.hash(password_sign_up)
    }
    collection.insert_one(new_usr_data)


  

def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    user = collection.find_one({"email": email_forgot_passwd})
    if user:
        return True, user['username']
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, username_forgot_passwd: str, email_forgot_passwd: str, company_name: str, random_password: str, reset_url: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(auth_token = auth_token)

    resp = client.send_message(
    message={
        "to": {
        "email": email_forgot_passwd
        },
        "content": {
        "title": company_name + ": Senha temporária!",
        "body": "Olá, " + username_forgot_passwd + "!" + "\n" + "\n" + "\nSua senha temporária de login é: " + random_password  + "\n" + "\n" + "{{info}}"
        },
        "data":{
        "info": "Por favor, resete sua senha o quanto antes em:  " + reset_url + ""
        }
    }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    user = collection.find_one({"email": email_})
    if user:
        user['password'] = ph.hash(random_password)
        collection.update_one({"_id": user["_id"]}, {"$set": user})
    

def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when 
    resetting the password.
    """
    user = collection.find_one({"email": email_reset_passwd})
    if user:
        try:
            if ph.verify(user['password'], current_passwd):
                return True
        except:
            pass
    return False












