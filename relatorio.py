# relatorio.py

import os
import streamlit as st
import datetime

def salvar_relatorio(cpf):
    """
    Salva informações de busca no arquivo de relatório.

    Args:
        cpf (str): O CPF pesquisado.
    """
    try:
        now = datetime.datetime.now()
        data_hora = now.strftime("%Y-%m-%d %H:%M:%S")

        with open('relatorio.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'Data e Hora da Busca: {data_hora}\n')
            arquivo.write(f'CPF Pesquisado: {cpf}\n')
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o relatório: {str(e)}")


def criar_relatorio(cpf):
    try:
        with open('relatorio.txt', 'a', encoding='utf-8') as arquivo_relatorio:
            arquivo_relatorio.write(cpf + '\n')  # Adicione o CPF ao arquivo de relatório
    except Exception as e:
        st.error(f"Erro ao criar relatório: {str(e)}")

def exibir_relatorio():
    try:
        with open('relatorio.txt', 'r', encoding='utf-8') as arquivo_relatorio:
            linhas = arquivo_relatorio.readlines()

        if len(linhas) == 0:
            st.write("Nenhum CPF registrado no relatório.")
        else:
            st.header("CPF's Consultados:")
            for linha in linhas:
                cpf = linha.strip()
                st.write(cpf)
    except FileNotFoundError:
        st.error("O arquivo de relatório não foi encontrado.")

def excluir_relatorio():
    try:
        os.remove('relatorio.txt')
        st.success("Relatório excluído com sucesso.")
    except FileNotFoundError:
        st.error("O arquivo de relatório não foi encontrado.")
    except Exception as e:
        st.error(f"Erro ao excluir relatório: {str(e)}")
