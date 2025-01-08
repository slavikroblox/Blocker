import requests

# OUTDATED FILE
# Use FindGameData(universeID).data

def FindBadgesFromGame(universeID, cursor=None):
    api_url = f"https://badges.roblox.com/v1/universes/{universeID}/badges"

    params = {}
    if cursor:
        params['cursor'] = cursor

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        badges = data.get('data', [])
        next_cursor = data.get('cursor')

        for badge in badges:
            print(badge["name"], "|", badge["description"], "| Won yesterday:", badge["statistics"]["pastDayAwardedCount"], ", Won all time:", badge["statistics"]["awardedCount"])

        if next_cursor:
            print(f"Next cursor: {next_cursor}")
            FindBadgesFromGame(3647333358, next_cursor)
            
    else:
        print(f"Error: {response.status_code}, {response.text}")

    
FindBadgesFromGame(3647333358)