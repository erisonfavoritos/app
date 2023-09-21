import streamlit as st

credenciais = {'user': 'erisonfavoritos', 'senha': 'Aig189669'}


def login():
    st.sidebar.subheader("Login")

    senha_admin = "123"
    senha = st.sidebar.text_input("Senha", type="password")

    if senha == senha_admin:
        st.sidebar.success("Login realizado com sucesso!")
        return True
    elif senha != "":
        st.sidebar.error("Senha incorreta. Por favor, insira a senha correta.")

    # Verifique se o login não foi bem-sucedido ou se nenhuma senha foi inserida antes de esconder o campo de senha.
    if senha != senha_admin or senha == "":
        return False

