import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL сервера
server_url = "https://www.gs4u.net/en/s/358042.html"

# Имя базы данных SQLite
db_name = "server_players.db"

# Определение модели игрока
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Создание двигателя базы данных
engine = create_engine(f'sqlite:///{db_name}')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Функция для получения списка игроков с сервера
def get_server_players(url):
    # response = requests.get(url)
   # content = response.content
    content = "<html></html>"
    with open('mock/index_1_players.html', 'r') as file:
        content = file.read()
    BeautifulSoup(content, 'html.parser')
    soup = BeautifulSoup(content, 'html.parser')

    # Найти таблицу с игроками
    table = soup.find('table', class_='serverplayers tablesorter table table-striped table-hover')

    # Извлечь имена игроков из таблицы
    players = []
    if table is not None:
        for row in table.find_all('tr'):
            print("row.find('td')", row.find('td'))
            if row.find('td') != None:
                player_name = row.find('td').text
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

if __name__ == '__main__':

    # Основная часть программы
    while True:
        # Получить текущий список игроков
        current_players = get_server_players(server_url)
        print("current_players", current_players)

        # Проверить на наличие новых игроков
        new_players = check_new_players(current_players)

        # Вывести результаты
        if new_players:
            print(f"{datetime.now()}: Новые игроки: {', '.join(new_players)}")

        # Пауза на 2 минуты
        time.sleep(120)

