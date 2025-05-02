import requests
from bs4 import BeautifulSoup
import pandas as pd

# Collects VLR Game Stats for each individual match
def get_data(game_id):
    url = f"https://www.vlr.gg/{game_id}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    players = []
    ratings = []
    count = 0
    
    tables = soup.find_all('table', class_='wf-table-inset mod-overview')

    for table in tables:
        for row in table.find_all('tr'):
            columns = row.find_all('td')

            for col in columns:
                if 'mod-player' in col.get('class'):
                    player_name = col.find('div', class_='text-of')
                    if player_name and 0 <= count < 120 or 239 < count < 480:
                        #players.append(player_name.text.strip())
                        data.append([player_name.text.strip()])

                if 'mod-stat' in col.get('class') and 'mod-agents' not in col.get('class'):
                    mod_both_span = col.find('span', class_='mod-both')
                    if mod_both_span:
                        value = mod_both_span.text.strip()
                        if 0 <= count < 120 or 239 < count < 480:
                            if 0 <= count < 120:
                                data[count // 12].append(value)
                            elif 239 < count < 480:
                                data[count // 12 - 10].append(value)
                            #ratings.append(value)
                        count += 1

    scores = soup.find_all('div', class_='score')
    rounds = [score.text.strip() for score in scores]
    for i in range(len(rounds)):
        rounds[i] = int(rounds[i])
    total_rounds = sum(rounds)

    for i in range(len(data)):
        data[i].append(total_rounds)

    return data
    
def convert_to_df(data):
    df = pd.DataFrame(data)
    df.columns = ['Player', 'Rating', 'ACS', 'Kills', 'Deaths', 'Assists', '+/-','KAST', 'ADR', 'HS%', 'FK', 'FD', 'FK-Diff', 'Rounds']
    #print(df)
    df.to_csv('map_stage1_stats.csv', index=False)

if __name__=="__main__":
    n = 459517
    big_data = []
    while n < 459547:
        stats = get_data(n)
        for i in range(len(stats)):
            big_data.append(stats[i])
        n = n + 1

    n = 458805
    while n < 458836:
        stats = get_data(n)
        for i in range(len(stats)):
            big_data.append(stats[i])
        n = n + 1

    n = 450057
    while n < 450077:
        stats = get_data(n)
        for i in range(len(stats)):
            big_data.append(stats[i])
        n = n + 1

    n = 459826
    while n < 459856:
        stats = get_data(n)
        for i in range(len(stats)):
            big_data.append(stats[i])
        n = n + 1
    convert_to_df(big_data)