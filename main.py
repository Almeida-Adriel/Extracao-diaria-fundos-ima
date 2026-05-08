import os
import pandas as pd
from src.scraper import AnbimaScraper
from src.processor import processar_ima, processar_idka, consolidar_final, transformar_para_armazenamento
from src.utils import swap_decimal_separator

def run_pipeline():
    scraper = AnbimaScraper()
    try:
        html_ima = scraper.get_ima_html()
        df_ima, map_ima = processar_ima(html_ima)
        
        html_idka = scraper.get_idka_html()
        df_idka, map_idka = processar_idka(html_idka, df_ima, map_ima)
        
        total_map = {**map_ima, **map_idka}
        
        df_final = consolidar_final(df_ima, df_idka, total_map)

        df_para_salvar = transformar_para_armazenamento(df_final)
        
        parquet_path = 'data/historico_fundos.parquet'
        excel_path = 'data/historico_fundos.xlsx'

        if os.path.exists(parquet_path):
            df_antigo = pd.read_parquet(parquet_path)
            # Evita duplicar a mesma data se rodar o script 2x no mesmo dia
            df_consolidado = pd.concat([df_antigo, df_para_salvar]).drop_duplicates(subset=['Data de Referência'], keep='last')
        else:
            df_consolidado = df_para_salvar

        df_consolidado.to_parquet(parquet_path, index=False)
        
        df_consolidado.to_excel(excel_path, index=False)
        
        print(f"Dados salvos com sucesso para a data: {df_para_salvar['Data de Referência'].iloc[0]}")
        
    finally:
        scraper.quit()

if __name__ == "__main__":
    run_pipeline()