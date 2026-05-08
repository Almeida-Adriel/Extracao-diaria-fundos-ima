from io import StringIO
from . import utils
import pandas as pd
import time

def processar_ima(html_source):
    time.sleep(2)
    tabelas = pd.read_html(StringIO(html_source), thousands='.', decimal=',')
    df_pivot_ima = pd.DataFrame()
    if tabelas:
        for tabela in tabelas:
            if 'Variação Diária (%)' in str(tabela.values):
                df_ima = tabela.iloc[9:18].copy()
                
                # Criando o Pivot para o IMA
                df_resumo = df_ima[['Índice', 'Data de Referência', 'Variação Diária (%)']].copy()
                df_pivot_ima = df_resumo.pivot(index='Data de Referência', columns='Índice', values='Variação Diária (%)')
                
                # Guardando os Números Índices
                indices_map = df_ima.set_index('Índice')['Número Índice'].to_dict()
                break
    
    return df_pivot_ima, indices_map

def processar_idka(html_source, df_pivot_ima=None, indices_map=None):
    time.sleep(2)
    tabelas = pd.read_html(StringIO(html_source), thousands='.', decimal=',')
    df_pivot_idka = pd.DataFrame()
    if indices_map is None:
        indices_map = {}
    if tabelas:
        for tabela in tabelas:
            if 'IPCA' in str(tabela.values):
                df_idka_raw = tabela.iloc[15:22, :3].copy()
                df_idka_raw.columns = ['NOME', 'N INDICE', 'VARIAÇÃO DIÁRIA']
                
                data_ref = df_pivot_ima.index[0] if (df_pivot_ima is not None and not df_pivot_ima.empty) else time.strftime('%d/%m/%Y')
                
                # Pivotando IDkA
                df_idka_raw['Data'] = data_ref
                df_pivot_idka = df_idka_raw.pivot(index='Data', columns='NOME', values='VARIAÇÃO DIÁRIA')
                
                # Mapeando índices do IDkA para a linha de baixo
                idka_indices_map = df_idka_raw.set_index('NOME')['N INDICE'].to_dict()
                indices_map.update(idka_indices_map)
                break
    
    return df_pivot_idka, indices_map

def consolidar_final(df_ima, df_idka, indices_map):
    df_final_consolidado = pd.concat([df_ima, df_idka], axis=1)
    df_final_consolidado.reset_index(inplace=True)
    df_final_consolidado.rename(columns={df_final_consolidado.columns[0]: 'Data de Referência'}, inplace=True)

    # Adiciona a linha de "Número Índice"
    row_num_idx = {'Data de Referência': 'Número Índice'}
    for col in df_final_consolidado.columns:
        if col != 'Data de Referência':
            row_num_idx[col] = indices_map.get(col, '')

    df_final_consolidado = pd.concat([df_final_consolidado, pd.DataFrame([row_num_idx])], ignore_index=True)

    df_final_consolidado = df_final_consolidado[
        ['Data de Referência', 'IRF-M 1', 'IRF-M 1+', 
        'IRF-M', 'IMA-B 5', 'IMA-B 5+',
        'IMA-B', 'IMA-S', 'IMA-GERAL ex-C', 
        'IMA-GERAL', 'IDkA IPCA 2A', 'IDkA IPCA 3A', 
        'IDkA IPCA 5A', 'IDkA IPCA 10A', 'IDkA IPCA 15A', 
        'IDkA IPCA 20A', 'IDkA IPCA 30A'
        ]]

    # Formatação Final (Vírgulas e %)
    cols_valores = [c for c in df_final_consolidado.columns if c != 'Data de Referência']
    # Linha 0: Variações (%)
    df_final_consolidado.iloc[0, 1:] = df_final_consolidado.iloc[0, 1:].apply(lambda x: utils.swap_decimal_separator(x, True))
    # Linha 1: Números Índice
    df_final_consolidado.iloc[1, 1:] = df_final_consolidado.iloc[1, 1:].apply(lambda x: utils.swap_decimal_separator(x, False))

    return df_final_consolidado
    
def transformar_para_armazenamento(df_final):
    data_ref = df_final.iloc[0, 0]
    
    # Criamos um dicionário começando pela Data
    row_data = {'Data de Referência': data_ref}
    
    # Iteramos pelas colunas de índices (pulando a primeira que é a data)
    for col in df_final.columns[1:]:
        var_diaria = df_final.iloc[0][col]
        num_indice = df_final.iloc[1][col]
        
        # Criamos colunas específicas para cada métrica
        row_data[f'{col} | Var %'] = var_diaria
        row_data[f'{col} | Índice'] = num_indice

    return pd.DataFrame([row_data])