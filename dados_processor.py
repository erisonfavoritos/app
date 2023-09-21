# dados_processor.py
import pandas as pd

def process_data_pandas(df_perfil, df_consumidor, df_pedido, df_parcela, cpf_to_search):
    perfil_filtered = df_perfil[df_perfil["Cpf_cnpj"] == cpf_to_search]

    if perfil_filtered.empty:
        return {}

    perfil_id = perfil_filtered.iloc[0]["Id_perfil"]

    consumidor_filtered = df_consumidor[df_consumidor["id_perfil"] == perfil_id]

    if consumidor_filtered.empty:
        return {}

    consumidor_id = consumidor_filtered.iloc[0]["id_consumidor"]

    pedido_filtered = df_pedido[(df_pedido["id_consumidor"] == consumidor_id) & (df_pedido["ativo"] == True)]

    if pedido_filtered.empty:
        return {}

    found_pedido_ids = pedido_filtered["id_pedido"].tolist()
    resultado = {}

    for pedido_id in found_pedido_ids:
        parcelas = df_parcela[df_parcela["id_pedido"] == pedido_id]

        # Filtrar parcelas que não possuem as chaves "valor_pago" e "data_pagamento"
        filtered_parcelas = parcelas[
            ~parcelas[["valor_pago", "data_pagamento"]].notnull().any(axis=1) &
            (parcelas["ativo"] == True)
        ]

        if not filtered_parcelas.empty:
            parcela_ids = filtered_parcelas["id_pedido_parcela"].tolist()
            resultado[pedido_id] = parcela_ids

    return resultado

def pedidos_filtrados_detalhados(final_result, df_pedido_item, df_produto_servico):
    detalhes_pedidos = {}

    for pedido_id, parcela_ids in final_result.items():
        detalhes_pedido = {
            "id_pedido_item": [],
            "quantidade": [],
            "descricao": [],
            "preco_venda": [],
            "ativo": []
        }

        for parcela_id in parcela_ids:
            pedido_item_info = df_pedido_item[df_pedido_item["id_pedido"] == pedido_id]

            if not pedido_item_info.empty:
                ativo_items = pedido_item_info[pedido_item_info["ativo"] == True]

                if not ativo_items.empty:
                    detalhes_pedido["id_pedido_item"].extend(ativo_items["id_pedido_item"].tolist())
                    detalhes_pedido["quantidade"].extend(ativo_items["quantidade"].tolist())

                    produto_ids = ativo_items["id_produto_servico"].tolist()
                    produto_info = df_produto_servico[df_produto_servico["id_produto_servico"].isin(produto_ids)]
                    detalhes_pedido["descricao"].extend(produto_info["descricao"].tolist())
                    detalhes_pedido["preco_venda"].extend(produto_info["preco_venda"].tolist())

                    # Adiciona o status "ativo" do item
                    detalhes_pedido["ativo"].extend(ativo_items["ativo"].tolist())

        detalhes_pedidos[pedido_id] = detalhes_pedido

    return detalhes_pedidos
