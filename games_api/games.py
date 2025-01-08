import requests
from timeconverter import *
from numbershorter import *

class GameData:
    def __init__(self, universeID, playing=0, visits=0, name=None, creator=None, created=0, updated=0, isCreatorGroup=None, favorites=0, mpps=0, genre=None):
        self.universeID = universeID  # Universe ID of the game
        self.playing = playing  # How many players are playing the game
        self.visits = visits  # How many players visited the game
        self.name = name  # Gets name of the game
        self.creator = creator  # Gets name of the creator (name of the group or username)
        self.created = created  # Date of creating the game
        self.updated = updated  # Date of last updating the game
        self.isCreatorGroup = isCreatorGroup  # Checks if creator is group or user
        self.favorites = favorites  # Favorites count on game
        self.mpps = mpps  # Max Players Per Server
        self.genre = genre  # Genre of the game (All, horror, etc.)

    def __str__(self):
        # String representation of what prints if none parameter after FindGameData() (like .name) is provided
        return (f"Game Name: {self.name}\n"
                f"Creator: {self.creator}\n"
                f"Playing: {self.playing}\n"
                f"Visits: {self.visits}\n"
                f"Created: {self.created}\n"
                f"Updated: {self.updated}\n"
                f"Is Creator Group: {self.isCreatorGroup}\n"
                f"Favorites: {self.favorites}\n"
                f"Max Players: {self.mpps}\n"
                f"Genre: {self.genre}")

class Games:
    def __init__(self):
        self.games = {}  # Stores the game data

    def FindDataAboutGame(self, universeID):
        api_url = f"https://games.roblox.com/v1/games?universeIds={universeID}"

        if universeID not in self.games:
            self.games[universeID] = GameData(universeID)

        try:  # Trying to get the data, if it failed, it prints an error
            response = requests.get(api_url)  # Sends request to the URL, then returns the result
            response.raise_for_status()

            data = response.json()  # Converts data to JSON
        
            first_game = data["data"][0]

            name = first_game.get("name")
            self.games[universeID].name = name

            creator = first_game.get("creator")        
            creator = creator.get("name")
            self.games[universeID].creator = creator

            playing = first_game.get("playing")
            playing = shorter_number(playing)
            self.games[universeID].playing = playing

            visits = first_game.get("visits")
            visits = shorter_number(visits)
            self.games[universeID].visits = visits

            created = first_game.get("created")
            converted_time = ConvertTimestamp(created, desired_timezone='Etc/GMT-3')
            self.games[universeID].created = converted_time

            last_updated = first_game.get("updated")
            converted_time = ConvertTimestamp(last_updated, desired_timezone='Etc/GMT-3')
            self.games[universeID].updated = converted_time

            isCreatorGroup = first_game.get("creator").get("type")
            if isCreatorGroup == "Group":
                isCreatorGroup = "yes"
            else:
                isCreatorGroup = "no"
            self.games[universeID].isCreatorGroup = isCreatorGroup

            favorites = first_game.get("favoritedCount")
            favorites = shorter_number(favorites)
            self.games[universeID].favorites = favorites

            mpps = first_game.get("maxPlayers")
            self.games[universeID].mpps = mpps

            genre = first_game.get("genre")
            self.games[universeID].genre = genre

            

        except requests.exceptions.RequestException as error:  # If an error while getting data has occurred (most likely don't have access, or invalid URL)
            print("Request error:", error)

        return self.games[universeID]
    

    def FindBadgesFromGame(self, universeID, cursor=None):
        api_url = f"https://badges.roblox.com/v1/universes/{universeID}/badges"
        
        params = {}
        if cursor:
            params['cursor'] = cursor

        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            badges = data.get('data', [])
            next_cursor = data.get('nextPageCursor')

            for badge in badges:
                stats = badge.get('statistics')

                try:
                    wrp = int(stats.get('awardedCount', [])) / int(stats.get('pastDayAwardedCount', []))
                    wrp = round(wrp)
                    wrp = int(wrp * 5) / 100
                    if wrp > 80:
                        wrp = str(wrp) + "% (Super Easy :D )"
                    elif wrp > 60:
                        wrp = str(wrp) + "% (Easy :) )"
                    elif wrp > 30:
                        wrp = str(wrp) + "% (Normal :| )"
                    elif wrp > 20:
                        wrp = str(wrp) + "% (Hard :( )"
                    elif wrp > 10:
                        wrp = str(wrp) + "% (Insane >:( )"
                    else:
                        wrp = str(wrp) + "% (Impossible D:< )"
                except ZeroDivisionError:
                    wrp = "0% (Badge Closed)"

                print(
                    badge.get('name', []), 
                    "|", 
                    badge.get('description', []),
                    "| Won yesterday:", 
                    stats.get('pastDayAwardedCount', []), 
                    ", Won all time:", 
                    stats.get('awardedCount', []),
                    ", Win rate percentage:",
                    wrp
                )

            if next_cursor:
                # print(f"Next cursor: {next_cursor}")
                next_cursor
            else:
                print("No more data.")
        else:
            print(f"Error: {response.status_code}, {response.text}")


    def FavorGame(self, universeID, ROBLOSECURITY):
        url = f"https://games.roblox.com/v1/games/{universeID}/favorites"

        cookies = {'.ROBLOSECURITY': ROBLOSECURITY}

        logout_data = {
            'Accept': 'application/json',
            'Cookie': f'.ROBLOSECURITY={ROBLOSECURITY}'
        }
        h = requests.post("https://auth.roblox.com/v2/logout", headers=logout_data)
        csrf = h.headers.get("x-csrf-token")

        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf,
            "Referer": "https://games.roblox.com/v1/games/2587095324/favorites"
        })
        session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

        payload = {
            "isFavorited": True
        }

        response = session.post(url, json=payload)

        if response.status_code == 200:
            print("Successfully favorited game")
            print(response.text)
        else:
            print("Error:", response.status_code, ":", response.text)


    def UnfavorGame(self, universeID, ROBLOSECURITY):
        url = f"https://games.roblox.com/v1/games/{universeID}/favorites"

        cookies = {'.ROBLOSECURITY': ROBLOSECURITY}

        logout_data = {
            'Accept': 'application/json',
            'Cookie': f'.ROBLOSECURITY={ROBLOSECURITY}'
        }
        h = requests.post("https://auth.roblox.com/v2/logout", headers=logout_data)
        csrf = h.headers.get("x-csrf-token")

        print(csrf)

        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf,
            "Referer": "https://games.roblox.com/v1/games/2587095324/favorites"
        })
        session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

        payload = {
            "isFavorited": False
        }

        response = session.post(url, json=payload)

        if response.status_code == 200:
            print("Successfully unfavorited game")
        else:
            print("Error:", response.status_code, ":", response.text)

    def GetUniverseID(self, placeID):
        api_url = f"https://apis.roblox.com/universes/v1/places/{placeID}/universe"

        try:
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

            universeID = data["universeId"]

            print(f"UniverseID for PlaceID {placeID}: {universeID}")
            return universeID
        except:
            print("Unknown error")



