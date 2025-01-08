import requests


class AvatarData:
    def __init__(self, ROBLOSECURITY, scale=None):
        self.ROBLOSECURITY = ROBLOSECURITY  # Your .ROBLOSECURITY token
        self.scale = scale  # Gets scale of your avatar


class Avatar:
    def __init__(self):
        self.avatar = {}  # Stores your avatar data

    def GetAvatar(self, ROBLOSECURITY):
        url = "https://avatar.roblox.com/v2/avatar/avatar"

        if ROBLOSECURITY not in self.avatar:
            self.avatar[ROBLOSECURITY].ROBLOSECURITY = AvatarData(ROBLOSECURITY)

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
            "Referer": "https://avatar.roblox.com/v2/avatar/avatar"
        })
        session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

        response = session.get(url)
        data = response.json()

        scale = data["scales"]
        self.avatar[ROBLOSECURITY].scale = scale

        return self.users[ROBLOSECURITY]