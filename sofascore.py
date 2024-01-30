import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import time
import os
from datetime import datetime

# Define o cabeçalho para se identificar como um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Conecta ao banco de dados SQLite local (ou cria um novo se não existir)
conn = sqlite3.connect('C:/Users/Caina/Documents/Code-note/Sofascore2/static/{match_id}.db')
c = conn.cursor()

# Exclui a tabela statistics se ela já existir
c.execute('DROP TABLE IF EXISTS statistics')

# Cria uma nova tabela para armazenar os dados
c.execute('''
   CREATE TABLE statistics (
       id INTEGER PRIMARY KEY,
       timestamp TEXT,
       match_id INTEGER,
       expected_goals_home REAL,
       expected_goals_away REAL,
       ball_possession_home INTEGER,
       ball_possession_away INTEGER,
       total_shots_home INTEGER,
       total_shots_away INTEGER,
       shots_on_target_home INTEGER,
       shots_on_target_away INTEGER,
       passes_home INTEGER,
       passes_away INTEGER,
       big_chances_home INTEGER,
       big_chances_away INTEGER
   )
''')

# Salva as alteraç�es
conn.commit()

while True:
    # Inicializa todas as variáveis com um valor padrão
    expected_goals_home = 0
    expected_goals_away = 0
    ball_possession_home = 0
    ball_possession_away = 0
    total_shots_home = 0
    total_shots_away = 0
    shots_on_target_home = 0
    shots_on_target_away = 0
    passes_home = 0
    passes_away = 0
    big_chances_home = 0
    big_chances_away = 0

    # Faz a requisição para a API
    response = requests.get('https://api.sofascore.com/mobile/v4/event/{match_id}/statistics', headers=headers)

    # Converte o HTML retornado em um objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extrai os dados relevantes
    data = json.loads(soup.text)

    # Extrai o ID da partida da url da API
    match_id = response.url.split('/')[-2]

    # Atualiza os dados na tabela
    for group in data['periods'][0]['groups']:
        for item in group['statisticsItems']:
            if item['name'] == 'Expected goals':
                expected_goals_home = item['homeValue']
                expected_goals_away = item['awayValue']
            elif item['name'] == 'Ball possession':
                ball_possession_home = item['homeValue']
                ball_possession_away = item['awayValue']
            elif item['name'] == 'Total shots':
                total_shots_home = item['homeValue']
                total_shots_away = item['awayValue']
            elif item['name'] == 'Shots on target':
                shots_on_target_home = item['homeValue']
                shots_on_target_away = item['awayValue']
            elif item['name'] == 'Passes':
                passes_home = item['homeValue']
                passes_away = item['awayValue']
            elif item['name'] == 'Big chances':
                big_chances_home = item['homeValue']
                big_chances_away = item['awayValue']

    # Obtém o timestamp atual
    timestamp = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

    # Insere os dados na tabela
    c.execute('''
    INSERT INTO statistics (timestamp, match_id, expected_goals_home, expected_goals_away, ball_possession_home, ball_possession_away, total_shots_home, total_shots_away, shots_on_target_home, shots_on_target_away, passes_home, passes_away, big_chances_home, big_chances_away)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
    timestamp,
    int(match_id),
    expected_goals_home,
    expected_goals_away,
    ball_possession_home,
    ball_possession_away,
    total_shots_home,
    total_shots_away,
    shots_on_target_home,
    shots_on_target_away,
    passes_home,
    passes_away,
    big_chances_home,
    big_chances_away
    ))

    # Salva as alteraç�es
    conn.commit()

    # Aguarda 20 segundos antes de fazer a próxima requisição
    time.sleep(35)

# Fecha a conexão com o banco de dados
conn.close()
