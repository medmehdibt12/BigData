#!/usr/bin/python3
"""
Script de génération des datasets games_data.csv et players_data.csv
Nécessite: pip install faker pandas
"""

from faker import Faker
import random
from datetime import datetime, timedelta
import pandas as pd


def generate_game_info(n: int, fake: Faker) -> list:
    """Génère n jeux avec leurs informations"""

    publishers = [
        'Electronic Arts', 'Activision', 'Ubisoft', 'Nintendo',
        'Sony Interactive Entertainment', 'Microsoft Studios',
        'Take-Two Interactive', 'Rockstar Games', 'Square Enix',
        'Capcom', 'Sega', 'Bethesda Softworks',
        'Bandai Namco Entertainment', 'Konami', '2K Games',
    ]

    game_info = []
    for _ in range(n):
        game = {
            "GameID": fake.uuid4(),
            "Publisher": random.choice(publishers),
            "Rating": fake.random_element(elements=('E', 'T', 'M')),
            "Genre": random.choice(['MMO', 'FPS', 'RPG', 'Adventure', 'Strategy']),
            "Game_Length": fake.random_number(digits=2),
            "ReleaseDate": fake.date_between(
                start_date='-10y', end_date='today'
            ).isoformat(),
        }
        game_info.append(game)

    return game_info


def generate_player_activity(n: int, game_ids: list, fake: Faker) -> list:
    """Génère n enregistrements d'activité joueur"""

    player_activity = []
    for _ in range(n):
        start_time = fake.date_time_this_month()
        end_time = start_time + timedelta(minutes=random.randint(30, 300))

        activity = {
            "PlayerID": fake.uuid4(),
            "GameID": random.choice(game_ids),
            "SessionID": fake.uuid4(),
            "StartTime": start_time.isoformat(),
            "EndTime": end_time.isoformat(),
            "ActivityType": random.choice(['Playing', 'AFK', 'In-Queue']),
            "Level": random.randint(1, 100),
            "ExperiencePoints": float(random.randint(100, 10000)),
            "AchievementsUnlocked": random.randint(0, 10),
            "CurrencyEarned": float(random.randint(100, 5000)),
            "CurrencySpent": float(random.randint(0, 3000)),
            "QuestsCompleted": random.randint(0, 20),
            "EnemiesDefeated": random.randint(0, 50),
            "ItemsCollected": random.randint(0, 100),
            "Deaths": random.randint(0, 10),
            "DistanceTraveled": float(random.randint(1, 10000)),
            "ChatMessagesSent": random.randint(0, 100),
            "TeamEventsParticipated": random.randint(0, 5),
            "SkillLevelUp": random.randint(0, 10),
            "PlayMode": random.choice(['Solo', 'Co-op', 'PvP']),
        }
        player_activity.append(activity)

    return player_activity


def main():
    num_games = 50
    num_players = 100000

    fake = Faker()

    print(f"Génération de {num_games} jeux...")
    games = pd.DataFrame(generate_game_info(num_games, fake))

    print(f"Génération de {num_players} enregistrements de joueurs...")
    players = pd.DataFrame(
        generate_player_activity(num_players, games['GameID'].tolist(), fake)
    )

    games.to_csv('games_data.csv', index=False)
    players.to_csv('players_data.csv', index=False)

    print("✅ games_data.csv généré avec succès!")
    print(f"   → {len(games)} lignes, colonnes: {list(games.columns)}")
    print("\n✅ players_data.csv généré avec succès!")
    print(f"   → {len(players)} lignes, colonnes: {list(players.columns)}")


if __name__ == '__main__':
    main()