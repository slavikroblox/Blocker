import requests
from numbershorter import *

# OUTDATED FILE
# Use FindGameData(universeID).data

def FindVisitsFromGame(universeID):
    game_url = f"https://games.roblox.com/v1/games?universeIds={universeID}"

    try:
        response = requests.get(game_url)
        response.raise_for_status()

        data = response.json()
        
        if "data" in data and isinstance(data["data"], list) and data["data"]:
            first_game = data["data"][0]
            visits_value = first_game.get("visits")
            visits_shortered_number = shorter_number(visits_value)
            return("Visits:", visits_shortered_number)
        else:
            return("No games found or unexpected response format.")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)