import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

def baixar_boleto_uniguairaca():
    print("[Portal Acadêmico] Iniciando...")

    url_login      = os.getenv("PORTAL_LOGIN_URL")
    url_financeiro = os.getenv("PORTAL_URL")
    user  = os.getenv("PORTAL_USER")
    senha = os.getenv("PORTAL_PASS")
    pasta = os.getenv("PASTA_SAIDA")

    os.makedirs(pasta, exist_ok=True)

    prefs = {
        "download.default_directory": pasta,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }

    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 20)

    try:
        driver.get(url_login)
        print("[Portal Acadêmico] Página de login aberta.")

        wait.until(EC.presence_of_element_located((By.ID, "login")))
        driver.find_element(By.ID, "login").send_keys(user)
        driver.find_element(By.ID, "senha").send_keys(senha)
        driver.find_element(By.ID, "btn-login").click()
        print("[Portal Acadêmico] Login efetuado. Aguardando sessão...")
        time.sleep(4)

        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + "t")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])

        driver.get(url_financeiro)
        print("[Portal Acadêmico] Página financeiro aberta.")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        time.sleep(3)
        print("[Portal Acadêmico] Tabela carregada. Buscando boletos...")

        linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        indices_para_clicar = []

        for i, linha in enumerate(linhas):
            if "Em aberto" not in linha.text:
                continue
            botoes = linha.find_elements(
                By.XPATH,
                ".//button[contains(@class,'btn-primary') and contains(.,'Boleto')]"
            )
            if botoes:
                indices_para_clicar.append(i)

        print(f"[Portal Acadêmico] {len(indices_para_clicar)} boleto(s) encontrado(s).")

        total_baixados = 0
        for idx in indices_para_clicar:
            try:
                linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
                linha_alvo = linhas[idx]
                botoes = linha_alvo.find_elements(
                    By.XPATH,
                    ".//button[contains(@class,'btn-primary') and contains(.,'Boleto')]"
                )
                if botoes:
                    print(f"[Portal Acadêmico] Baixando boleto {total_baixados + 1}...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", botoes[0])
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", botoes[0])
                    total_baixados += 1
                    time.sleep(4)

                    if len(driver.window_handles) > 2:
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(1)
            except Exception as e_linha:
                print(f"[Portal Acadêmico] ⚠️  Erro na linha {idx + 1}: {e_linha}")
                continue

        if total_baixados == 0:
            print("[Portal Acadêmico] ⚠️  Nenhum boleto baixado.")
        else:
            print(f"[Portal Acadêmico] ✅ {total_baixados} boleto(s) baixado(s) em: {pasta}")

    except Exception as e:
        print(f"[Portal Acadêmico] ❌ Erro: {e}")
    finally:
        driver.quit()
