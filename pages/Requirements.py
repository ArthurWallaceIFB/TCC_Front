import streamlit as st

st.title("Requisitos para Web Crawling")

st.write("- URL Inicial")
st.caption("https://www.ifb.edu.br/espaco-do-estudante/estagio/boletins-de-estagio/36579-boletim-de-estagio-n-40-2013-vagas-de-30-10-a-3-11")

st.write("- Dominios permitidos de busca")
st.caption(["www.ifb.edu.br", "ifb.edu.br", "processoseletivo.ifb.edu.br"])

st.write('- Profundidade de busca')
st.caption("Ex: DEPTH_LIMIT: 2")

st.write('- Delay entre cada request')

st.write('- Quantidade máxima de requests assíncronos')

st.write("- Tipos de arquivos aceitos (.PDF)")