import streamlit as st
from packages.streamlit_login.widgets import __login__

# st.set_page_config(
#     page_title="Login - IFBots",
#     page_icon="🤖"
# )

__login__obj = __login__(auth_token = "pk_prod_XNB7MJGSQX4EMBHXE0K17EZE8FCA", 
                    company_name = "IFBots",
                    width = 200, height = 250, 
                    logout_button_name = 'Sair',
                    hide_menu_bool = True, 
                    hide_footer_bool = True, 
                    hide_sidebar_itens_bool = True,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json',
                    password_reset_url = st.secrets["PASSWORD_RESET_URL"])

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    __login__obj.show_sidebar_itens()
    st.markdown("Your Streamlit Application Begins here!")