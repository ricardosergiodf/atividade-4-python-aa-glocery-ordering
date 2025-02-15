import logging
import datetime
import os
import sys
import traceback
from botcity.web import WebBot, Browser, By
from selenium.webdriver.common.by import By
import pandas as pd
from botcity.maestro import *
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys

def setup_logging():
    log_path = "C:/Users/ricar/Desktop/-/Compass/atividades-praticas-compass/Sprint-4/ativ-pratica-4-python-aa/resources/logfiles"
    # Verifica se a pasta "logfiles" existe, se não, cria-a
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    data_atual = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    nome_arquivo_log = f"{log_path}/logfile-{data_atual}.txt"

    logging.basicConfig(
        filename=nome_arquivo_log,
        level=logging.INFO,
        format="(%(asctime)s) - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )


def bot_driver_setup():
    try:
        bot = WebBot()
        bot.headless = False
        bot.browser = Browser.EDGE
        bot.driver_path = r"C:\Users\ricar\Downloads\edgedriver_win64\msedgedriver.exe"
        return bot
    
    except Exception:
        error_exception()
        return None


def browse_url(bot, url):
    try:
        logging.info(f"Abrindo Browser na URL: {url}")
        return bot.browse(url)
    except Exception:
        error_exception()
        return False


def browse_close(bot):
    try:
        bot.key_esc()
        logging.info("Fechando Browser.")
        return bot.driver.quit()
    except Exception:
        error_exception()
        return False


def error_exception():
    exc_type, exc_value, exc_tb = sys.exc_info()  # Captura a exceção atual

    if exc_type:  # Verifica se há um erro capturado
        tb = traceback.extract_tb(exc_tb)  # Obtém detalhes do traceback
        last_trace = tb[-1]  # Última linha do traceback (onde o erro ocorreu)

        line_number = last_trace.lineno  # Número da linha do erro
        error_type = exc_type.__name__  # Tipo do erro (ex: ValueError, KeyError)
        error_message = str(exc_value)  # Mensagem do erro

        logging.error(f"Erro do tipo {error_type} na linha {line_number}: {error_message}.")
    else:
        logging.error("Erro não identificado.")

    return None


def community_login(bot, community_login_btn):
    try:
        logging.info("Carrega as credenciais salvas no .env")
        load_dotenv()

        logging.info("Se tiver o botao de cookies, captura e clica em aceitar.")
        cookie_btn = bot.find_element("onetrust-accept-btn-handler", By.ID)
        if cookie_btn:
            cookie_btn.click()

        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        logging.info("Clica no botao de login.")
        community_login_btn.click()

        logging.info("Preenche o email.")
        email_field = bot.find_element("/html[1]/body[1]/div[3]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/input[1]", By.XPATH)
        email_field.send_keys(email)

        logging.info("Clica em next.")
        next_btn = bot.find_element("button[type='button']", By.CSS_SELECTOR)
        next_btn.click()
        bot.wait(1000)

        logging.info("Preenche a senha.")
        password_field = bot.find_element("/html[1]/body[1]/div[3]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/input[1]", By.XPATH)
        password_field.send_keys(password)

        login_btn = bot.find_element(".slds-button.slds-button_brand.button", By.CSS_SELECTOR)
        login_btn.click()

        return True
    except Exception:
        error_exception()
        return False
    

def shopping_list(bot):
    try:
        bot.wait(1500)
        add_btn = bot.find_element("#add_button", By.CSS_SELECTOR)
        bot.wait(1500)
        add_btn.click()
        try:
            alert = bot.driver.switch_to.alert
            logging.info(f"Fechando o popup: {alert.text}")
            if alert:
                alert.accept()
        except Exception:
            logging.info("Popup nao encontrado.")

        logging.info("Captura e clica no botao de download.")
        download_list_btn = bot.find_element("//a [@class='btn btn-success' and @role='button']", By.XPATH)
        download_list_btn.click()

        bot.wait(1000)

        shopping_list_csv_path = "./shopping-list.csv"
        if not shopping_list_csv_path:
            raise FileNotFoundError("Lista do carrinho de compras .csv nao encontrada.")
        
        logging.info("Lendo o arquivo csv.")
        shopping_list_csv = pd.read_csv(shopping_list_csv_path)

        logging.info("Captura o campo de digitar o item e o botao de adicionar item.")
        enter_item = bot.find_element("#myInput", By.CSS_SELECTOR)

        for item, row in shopping_list_csv.iterrows():
            logging.info(f"Adiciona {row['Favorite Food']} na lista.")
            enter_item.send_keys(row['Favorite Food'])

            if add_btn.is_enabled():
                logging.info("Clica em adicionar item.")
                add_btn.click()
            else:
                logging.warning("O botão de adicionar item esta desabilitado.")
                

        logging.info("Captura e aceita o input dos termos.")
        agree_terms = bot.find_element("#agreeToTermsYes", By.CSS_SELECTOR)
        agree_terms.click()

        logging.info("Captura e clica no botao de submit.")
        submit_btn = bot.find_element("#submit_button", By.CSS_SELECTOR)
        submit_btn.click()

        bot.wait(2000)

        return True
    except Exception:
        error_exception()
        return False