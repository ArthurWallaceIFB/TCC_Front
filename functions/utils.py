# utils.py
from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st

class Utils:
    def __init__(self):
        # Configuração do EncryptedCookieManager
        self.cookies = EncryptedCookieManager(
            prefix="streamlit_login_ui_yummy_cookies",
            password='9d68d6f2-4258-45c9-96eb-2d6bc74ddbb5-d8f49cab-edbb-404a-94d0-b25b1d4a564b'
        )
        if not self.cookies.ready():
            st.stop()  

    def get_decrypted_cookie(self, cookie_name):
        """
        Retorna o valor descriptografado de um cookie.
        """
        
        if cookie_name in self.cookies.keys():
            return self.cookies[cookie_name]
        else:
            return None
    
    def show_logout(self):
        if st.session_state['LOGGED_IN'] == True:
            del_logout = st.sidebar.empty()
            del_logout.markdown("#")
            logout_click_check = del_logout.button("Sair")

            if logout_click_check == True:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                self.cookies['__streamlit_login_signup_ui_username__'] = '1c9a923f-fb21-4a91-b3f3-5f18e3f01182'
                del_logout.empty()
                st.rerun()

# Instância única da classe Utils para ser usada em outros scripts
utils_instance = Utils()

# Ao importar utils.py diretamente, utils_instance está disponível imediatamente
get_decrypted_cookie = utils_instance.get_decrypted_cookie
show_logout = utils_instance.show_logout
