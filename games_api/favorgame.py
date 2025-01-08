import requests
import json


def FavorGame(universeID, ROBLOSECURITY):
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
    else:
        print("Error:", response.status_code, ":", response.text)


def UnfavorGame(universeID, ROBLOSECURITY):
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
        "isFavorited": False
    }

    response = session.post(url, json=payload)

    if response.status_code == 200:
        print("Successfully unfavorited game")
    else:
        print("Error:", response.status_code, ":", response.text)


