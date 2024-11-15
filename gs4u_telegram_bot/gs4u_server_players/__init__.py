import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()
SERVER_GS4U_URL = os.getenv("SERVER_GS4U_URL")

DB_FILE_PATH=os.getenv("DB_FILE_PATH")
# URL сервера
server_url = SERVER_GS4U_URL

# Имя базы данных SQLite
db_name = "server_players.db"

# Определение модели игрока
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Создание двигателя базы данных
engine = create_engine(f'sqlite:///{DB_FILE_PATH}')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Функция для получения списка игроков с сервера
def get_server_players(url):
    response = requests.get(url)
    print(response.status_code)
    content = response.content
    # content = "<html></html>"
    # with open('mock/index_tdm_players.html', 'r') as file:
    #      content = file.read()
    soup = BeautifulSoup(content, 'html.parser')

    # Find all tables with the specified class
    tables = soup.find_all('table', class_='serverplayers tablesorter table table-striped table-hover')

    players = []
    for table in tables:
        # Extract player names from each table
        for row in table.find_all('tr'):
            if row.find('td') is not None:
                player_name = row.find('td').text.strip() #Added strip() to remove leading/trailing whitespace
                players.append(player_name)


    return players

# Функция для проверки новых игроков
def check_new_players(current_players):
    new_players = []
    for player in current_players:
        # Проверить, есть ли игрок в базе данных
        existing_player = session.query(Player).filter_by(name=player).first()
        if not existing_player:
            new_players.append(player)
            # Добавить нового игрока
            new_player = Player(name=player)
            session.add(new_player)
            session.commit()
    return new_players

# Функция для обновления таблицы игроков
def update_player_table(current_players):
    # Удалить существующих игроков из базы данных
    session.query(Player).delete()
    session.commit()

    # Добавить всех текущих игроков в базу данных
    for player in current_players:
        new_player = Player(name=player)
        session.add(new_player)
    session.commit()

if __name__ == '__main__':
    # Основная часть программы
    while True:
        # Получить текущий список игроков
        current_players = get_server_players(server_url)
        print("current_players", current_players)

        # Проверить на наличие новых игроков
        new_players = check_new_players(current_players)

        # Обновить таблицу игроков
        update_player_table(current_players)

        # Вывести результаты
        if new_players:
            message = f"Зашли игроки: {', '.join(new_players)}"
            print(f"{datetime.now()}: {message}")


        time.sleep(20)
