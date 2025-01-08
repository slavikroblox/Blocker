import requests
import json

def createVipServer(placeID, name, price, ROBLOSECURITY):
    url = f"https://games.roblox.com/v1/games/vip-servers/{placeID}"

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
        "Referer": url
    })
    session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

    payload = {
        "name": str(name),
        "expectedPrice": int(price),
        "isPurchaseConfirmed": True
    }

    confirm = str(input("Confirm your VIP server purchase (Y/N): "))

    if confirm == "Y":
        response = session.post(url, json=payload)
        if response.status_code == 200:
            print("Successfully created VIP server")
        else:
            print("Error:", response.text)
    elif confirm == "N":
        print("Purchase canceled")
    else:
        print("Unknown")