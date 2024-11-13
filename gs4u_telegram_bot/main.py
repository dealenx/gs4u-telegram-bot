import os
from datetime import datetime
import time
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

from gs4u_telegram_bot.telegram_bot import run_bot

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
import urllib, requests
from gs4u_telegram_bot import gs4u_server_players

load_dotenv()
SERVER_GS4U_URL = os.getenv("SERVER_GS4U_URL")
# URL сервера
server_url = SERVER_GS4U_URL



def run():
    # Основная часть программы
    while True:
        # Получить текущий список игроков
        current_players = gs4u_server_players.get_server_players(server_url)
        print("current_players", current_players)

        # Проверить на наличие новых игроков
        new_players = gs4u_server_players.check_new_players(current_players)

        # Обновить таблицу игроков
        gs4u_server_players.update_player_table(current_players)

        # Вывести результаты
        if new_players:
            message = f"Зашли игроки: {', '.join(new_players)}"
            print(f"{datetime.now()}: {message}")

            url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
                f'{TELEGRAM_BOT_TOKEN}', f'{CHAT_ID}', urllib.parse.quote_plus(message))
            _ = requests.get(url, timeout=10)

        time.sleep(20)

if __name__ == '__main__':
    # run_bot()
    run()

