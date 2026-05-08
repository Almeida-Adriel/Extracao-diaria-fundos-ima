from src.scraper import AnbimaScraper
from src.processor import processar_ima, processar_idka, consolidar_final
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
        
        df_final.to_excel('data/fundos-ima.xlsx', index=False)
        
    finally:
        scraper.quit()

if __name__ == "__main__":
    run_pipeline()