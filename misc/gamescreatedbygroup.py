import requests
from timeconverter import *

def GamesCreatedByGroup(groupID):
    api_url = f"https://games.roblox.com/v1/groups/{groupID}/games"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        
        first_game = data["data"][0]
        name = first_game.get("name")
        print("Name: ", name)
        creator = first_game.get("creator")
        isGroup = creator.get("isGroup")         
        creator = creator.get("name")
        if isGroup == "true":
            print("Creator: ", creator, " (group)")
        else:
            print("Creator: ", creator)
        created = first_game.get("created")
        converted_time = ConvertTimestamp(created, desired_timezone='Etc/GMT-3')
        print("Created: ", converted_time, "(UTC+3)")
        last_updated = first_game.get("updated")
        converted_time = ConvertTimestamp(last_updated, desired_timezone='Etc/GMT-3')
        print("Last Updated: ", converted_time, "(UTC+3)")

    except requests.exceptions.RequestException as error:
        print("Request error:", error)