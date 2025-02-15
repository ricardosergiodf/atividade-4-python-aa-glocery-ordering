"""
Please make sure you install the bot dependencies with `pip install --upgrade -r requirements.txt`
"""

from botcity.maestro import *
from functions import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    maestro = BotMaestroSDK.from_sys_args()
    execution = maestro.get_execution()

    setup_logging()
    logging.info("Inicio - Atividade 4 - Python & Automation Anywhere - Online Glocery Ordering")

    if execution.task_id == 0:
        logging.info("Maestro desativado -> Executando localmente")
        maestro = None

    if maestro:
        print(f"Task ID is: {execution.task_id}")
        print(f"Task Parameters are: {execution.parameters}")

    url = "https://pathfinder.automationanywhere.com/challenges/AutomationAnywhereLabs-ShoppingList.html"

    bot = bot_driver_setup()

    browse_url(bot, url)
    
    community_login_btn = bot.find_element("/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[3]/a[1]/button[1]", By.XPATH)
    if community_login_btn:
        login = community_login(bot, community_login_btn)
        if not login:
            logging.info("Erro no Community Login.")
        else:
            logging.info("Community Login feito com sucesso.")

    shopping_cart = shopping_list(bot)
    if not shopping_cart:
        logging.info("Erro na adicao de itens ao carrinho.")
    else:
        logging.info("Shopping list feito com sucesso.")

    logging.info("Captura o resultado.")
    result_message = bot.find_element("success-title", By.ID).text
    if not result_message:
        raise AttributeError("Elemento 'resultado' nao encontrado, ocorreu algum erro.")
    logging.info(f"Resultado: {result_message}")

    try:
        browse_close(bot)
    except Exception:
        error_exception()

    logging.info("Fim.")


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
