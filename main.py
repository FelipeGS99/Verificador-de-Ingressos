from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from telegram import Bot
import time
import asyncio
from dotenv import load_dotenv
import os

# Configurações do Chrome

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

async def avisa_telegram(mensagem: str):
    """Envia mensagem via Telegram."""
    await bot.send_message(chat_id=CHAT_ID, text=mensagem)

options = Options()
options.add_argument('--log-level=3')  # Desativa logs do Chrome
#options.add_argument('--headless')  # Executa o Chrome em modo headless (sem interface gráfica)

# Inicializa o driver com o webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abre a página
url = "https://cart.spfcticket.net/saopaulofcxlibertadparconmebollibertadores_25"
driver.get(url)

time.sleep(3)  # Espera o carregamento da página

cookie_button = driver.find_element(By.CLASS_NAME, 'cc-btn.cc-dismiss')
cookie_button.click()  # Clica no botão de aceitar cookies

campo_cpf = driver.find_element(By.ID, "inputPromocode")
campo_cpf.send_keys("48483294850")  # Preenche o campo de CPF

while True:
    validar_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-outline-primary.px-4")
    validar_button.click()  # Clica no botão de validar

    time.sleep(10)  # Espera o carregamento da página

    setoresDesejados = ['ARQUIBANCADA NORTE', 'ARQUIBANCADA SUL', 'ARQUIBANCADA OESTE', 'ARQUIBANCADA LESTE']

    for setor in setoresDesejados:
        try:
            div_ingresso = driver.find_element(By.XPATH, f"//div[contains(@class,'line') and .//label[@class='nameAndLot' and contains(normalize-space(.),'{setor}')]]")
        except NoSuchElementException:
            print(f"Ingressos para {setor} não encontrados.")
            continue
        if 'Esgotado' in div_ingresso.text:
            print(f"Ingressos para {setor} estão esgotados.")
        else:
            print(f"Ingressos para {setor} estão disponíveis.")
        if 'Esgotado' not in div_ingresso.text and 'ARQUIBANCADA SUL' in div_ingresso.text:
            asyncio.run(avisa_telegram(f"Ingressos para {setor} estão disponíveis."))