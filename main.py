from flask import Flask, render_template, request
from riot_api import get_live_game_by_puuid
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Use the PUUID directly from environment variables
        encrypted_puuid = os.getenv('ENCRYPTED_PUUID')
        region = 'na1'  # Change to desired region if needed

        if not encrypted_puuid:
            print("PUUID not found in environment variables!")
            return render_template('index.html', error="PUUID not found in environment variables!")

        # Check if the summoner is in a live game
        live_game_data = get_live_game_by_puuid(region)
        if not live_game_data:
            # If no live game, display an appropriate message on the website and console
            print("This summoner is not currently in a live game.")
            return render_template('index.html', error="This Summoner is not currently in a live game.")

        # Print the live game data to the console
        print("Live Game Data:")
        print(f"Game ID: {live_game_data.get('gameId')}")
        print(f"Map ID: {live_game_data.get('mapId')}")
        print(f"Game Mode: {live_game_data.get('gameMode')}")
        print(f"Game Type: {live_game_data.get('gameType')}")
        print(f"Game Queue Config ID: {live_game_data.get('gameQueueConfigId')}")
        print(f"Platform ID: {live_game_data.get('platformId')}")
        print(f"Game Start Time: {live_game_data.get('gameStartTime')}")
        print(f"Game Length: {live_game_data.get('gameLength')}")

        # Print participants
        print("\nParticipants:")
        for participant in live_game_data.get('participants', []):
            print(f"Riot ID: {participant.get('riotId')}, Champion ID: {participant.get('championId')}, "
                  f"Team ID: {participant.get('teamId')}, Spell 1: {participant.get('spell1Id')}, "
                  f"Spell 2: {participant.get('spell2Id')}")

        return render_template('index.html', live_game_data=live_game_data)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
