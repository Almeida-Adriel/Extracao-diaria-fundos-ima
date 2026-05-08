from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AnbimaScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

    def _clicar_consultar(self):
        try: self.driver.switch_to.frame(0)
        except: pass
        botao = self.wait.until(EC.element_to_be_clickable((By.NAME, 'Consultar')))
        botao.click()
        self.driver.switch_to.default_content()

    def get_ima_html(self):
        self.driver.get('https://www.anbima.com.br/pt_br/informar/ima-resultados-diarios.htm')

        try:
            aceitar_termos = self.wait.until(EC.element_to_be_clickable((By.ID, 'LGPD_ANBIMA_global_sites__text__btn')))
            aceitar_termos.click()
        except:
            pass

        self._clicar_consultar()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
        return self.driver.page_source
    
    def get_idka_html(self):
        self.driver.get('https://www.anbima.com.br/pt_br/informar/consulta-idka.htm')

        self._clicar_consultar()
        self.driver.switch_to.frame(0)
        return self.driver.page_source

    def quit(self):
        self.driver.quit()