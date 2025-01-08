import requests
from numbershorter import *

# OUTDATED FILE
# Use FindGameData(universeID).data

def FindPlayingFromGame(universeID):
    game_url = f"https://games.roblox.com/v1/games?universeIds={universeID}"

    try:
        response = requests.get(game_url)
        response.raise_for_status()

        data = response.json()
        
        if "data" in data and isinstance(data["data"], list) and data["data"]:
            first_game = data["data"][0]
            playing_value = first_game.get("playing")
            playing_shorted_number = shorter_number(playing_value)
            return("People Playing:", playing_shorted_number)
        else:
            return("No games found or unexpected response format.")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)