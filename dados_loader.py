import json
import pandas as pd
import streamlit

@streamlit.cache_data()
def load_data(file_path):
    """
    Carrega dados de um arquivo JSON e retorna-os como um dicionário.

    Args:
        file_path (str): O caminho do arquivo JSON a ser carregado.

    Returns:
        dict: Um dicionário contendo os dados do arquivo JSON.
    """
    # Leitura do arquivo JSON
    with open('dados/backup1.json', encoding='utf-8') as arquivo_json:
        data = json.load(arquivo_json)
    return data

def create_dataframes(data):
    """
    Cria DataFrames a partir de um dicionário de dados.

    Args:
        data (dict): O dicionário de dados contendo várias listas.

    Returns:
        tuple: Um conjunto de DataFrames criados a partir dos dados.
    """
    # Criar DataFrames a partir dos dados
    df_perfil = pd.DataFrame(data["listPerfil"])
    df_consumidor = pd.DataFrame(data["listConsumidor"])
    df_pedido = pd.DataFrame(data["listPedido"])
    df_parcela = pd.DataFrame(data["listPedidoParcela"])
    df_pedido_item = pd.DataFrame(data["listPedidoItem"])
    df_produto_servico = pd.DataFrame(data["listProdutoServico"])

    return df_perfil, df_consumidor, df_pedido, df_parcela, df_pedido_item, df_produto_servico
