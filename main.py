import streamlit as st
import pandas as pd
from dados_loader import load_data, create_dataframes
from dados_processor import process_data_pandas, pedidos_filtrados_detalhados
from login import login  # Importa a função de login
from cpf_validator import validate_cpf  # Importa a função de validação de CPF
from relatorio import exibir_relatorio, excluir_relatorio, \
    salvar_relatorio  # Importa as funções relacionadas ao relatório

def formatar_valor(valor):
    return f'R$ {valor:.2f}'

def calcular_valor_total(prices):
    return formatar_valor(sum(prices))

def determinar_estado(parcela_info):
    # Implemente a lógica para determinar o estado com base nas informações da parcela
    # Retorne "paga", "pendente" ou "vencimento_expirado" com base nas suas regras
    # Por exemplo, você pode comparar a data de vencimento com a data atual para determinar se está vencida.
    # Esta função deve ser personalizada de acordo com a lógica do seu aplicativo.
    return "pendente"  # Exemplo: considera todas as parcelas como pendentes por padrão

def main():
    # Função para a página principal

    # Título e introdução
    st.title('*:rainbow[Aplicativo Dany Modas]*:sunglasses:')
    st.markdown(''':violet[Se houver divergências de informações ou cadastro incompleto, clique aqui em baixo]''')
    st.markdown("[clique aqui](https://api.whatsapp.com/send?phone=65992159153&text=Ol%C3%A1%20Dany%20,%20estou%20contatando%20pois%20conheci%20seu%20App%20Online%20e%20preciso%20de%20ajuda!)")

    # Barra lateral para inserir o CPF
    cpf_to_search = st.sidebar.text_input('Digite o CPF:')

    # Validação do CPF
    if cpf_to_search and not validate_cpf(cpf_to_search):
        st.sidebar.error('CPF inválido. Por favor, insira um CPF válido.')
        return

    # Botões de ação
    if st.sidebar.button('Buscar'):
        # Carregamento dos dados e criação dos DataFrames
        file_path = 'backup1.json'
        data = load_data(file_path)
        df_perfil, df_consumidor, df_pedido, df_parcela, df_pedido_item, df_produto_servico = create_dataframes(data)

        final_result = process_data_pandas(df_perfil, df_consumidor, df_pedido, df_parcela, cpf_to_search)

        if final_result:
            st.write("ABAIXO SEGUE A[S] PARCELA[S] EM ABERTO")
            # Exibição das informações das parcelas em aberto
            for pedido_id, parcela_ids in final_result.items():
                st.write(f":orange[Parcela referente a este Pedido ID: {pedido_id}]")
                for parcela_id in parcela_ids:
                    parcela_info = df_parcela[df_parcela["id_pedido_parcela"] == parcela_id].iloc[0]
                    nro_parcela = parcela_info["nro_parcela"]
                    valor_parcela = formatar_valor(parcela_info["valor_parcela"])

                    # Formata a data para "dd-mm-YYYY"
                    data_vencimento = pd.to_datetime(parcela_info["data_vencimento"]).strftime("%d-%m-%Y")

                    # Exibe as informações da parcela
                    st.write(f":orange[Parcela {nro_parcela}: Valor {valor_parcela}, Vencimento - {data_vencimento}]")

                    # Determine o estado da parcela (paga, pendente ou vencimento expirado)
                    estado = determinar_estado(parcela_info)

                    # Exibe a legenda correspondente ao estado
                    if estado == "paga":
                        st.write("Estado da Parcela: ✅ Paga")
                    elif estado == "pendente":
                        st.write("Estado da Parcela: ⚠️ Pendente")
                    elif estado == "vencimento_expirado":
                        st.write("Estado da Parcela: ❌ Vencimento Expirado")

            detalhes_pedidos = pedidos_filtrados_detalhados(final_result, df_pedido_item, df_produto_servico)

            if detalhes_pedidos:
                #st.write("Detalhes dos pedidos:")
                # Exibição dos detalhes dos pedidos
                for pedido_id, detalhes_pedido in detalhes_pedidos.items():
                    st.write(f"Detalhes do Pedido ID: {pedido_id}")
                    detalhes_df = pd.DataFrame({
                        'Quantidade': detalhes_pedido["quantidade"],
                        'Descrição': detalhes_pedido["descricao"],
                        'Preço de Venda': [formatar_valor(preco) for preco in detalhes_pedido["preco_venda"]]
                    })

                    # Oculta as colunas 'index' e 'Item ID'
                    detalhes_df = detalhes_df.rename_axis(None)

                    # Adicione uma linha para exibir o valor total
                    detalhes_df.loc[len(detalhes_df)] = ["VALOR TOTAL", "",
                                                         calcular_valor_total(detalhes_pedido["preco_venda"])]

                    # Exibe o DataFrame com as colunas desejadas
                    st.dataframe(detalhes_df)
            else:
                st.write("Nenhum Pedido Encontrado.")
        else:
            st.write("Nenhum Pedido Encontrado, Por isso não consta parcela em aberto para o CPF informado.")

        # Após buscar informações, salve no relatório
        salvar_relatorio(cpf_to_search)

    # Checkbox para exibir ou ocultar opções de Admin
    admin_mode = st.sidebar.checkbox('Admin')

    if admin_mode:
        st.sidebar.write("Funcionalidades do Admin:")

        exibir_relatorio_checkbox = st.sidebar.checkbox('Exibir Relatório')
        excluir_relatorio_checkbox = st.sidebar.checkbox('Excluir Relatório')

        if exibir_relatorio_checkbox:
            if login():
                exibir_relatorio()

        if excluir_relatorio_checkbox:
            if login():
                excluir_relatorio()

if __name__ == "__main__":
    main()
