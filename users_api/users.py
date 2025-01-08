import requests
from timeconverter import ConvertTimestamp


class UserData:
    def __init__(self, userID, username=None, displayName=None, description=None, created=0, isBanned=None, extAppDisName=None, hasVerifiedBadge=None):
        self.userID = userID  # User ID
        self.username = username  # Username of user
        self.displayName = displayName  # Gets display name of user
        self.description = description  # Gets description of user
        self.created = created  # Gets date of profile creating
        self.isBanned = isBanned  # Checks if user is banned
        self.externalAppDisplayName = extAppDisName  #
        self.isVerified = hasVerifiedBadge  # Checks if user have verified badge

class Users:
    def __init__(self):
        self.users = {}  # Stores the user data

    def FindDataAboutUser(self, userID):
        api_url = f"https://users.roblox.com/v1/users/{userID}"

        if userID not in self.users:
            self.users[userID] = UserData(userID)

        try:  # Trying to get the data, if it didn't, it prints an error
            response = requests.get(api_url)  # Sends request to the URL, then returns the result
            response.raise_for_status()

            data = response.json()  # Converts data to JSON
        
            username = data["name"]
            self.users[userID].username = username

            displayName = data["displayName"]
            self.users[userID].displayName = displayName

            description = data["description"]
            self.users[userID].description = description

            created = data["created"]
            created = ConvertTimestamp(created)
            self.users[userID].created = created

            isBanned = data["isBanned"]
            self.users[userID].isBanned = isBanned

            extAppDisName = data["externalAppDisplayName"]
            self.users[userID].externalAppDisplayName = extAppDisName

            isVerified = data["hasVerifiedBadge"]
            self.users[userID].isVerified = isVerified


        except requests.exceptions.RequestException as error:  # If an error while getting data has occurred (most likely don't have access, or invalid URL)
            print("Request error:", error)

        return self.users[userID]
    
    def SetDisplayName(self, userID, displayName, ROBLOSECURITY):
        url = f"https://users.roblox.com/v1/users/{userID}/display-names"

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
            "Referer": f"https://users.roblox.com/v1/users/{userID}/display-names"
        })
        session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

        data = {
            "newDisplayName": displayName
        }

        response = session.patch(url, json=data)

        if response.status_code == 200:
            print("Successfully set display name")
        else:
            print("Error:", response.status_code, ":", response.text)

    def SetGender(self, gender, ROBLOSECURITY):
        url = "https://users.roblox.com/v1/gender"

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
            "Referer": "https://users.roblox.com/v1/gender"
        })
        session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

        data = {
            "gender": gender
        }

        response = session.post(url, json=data)

        if response.status_code == 200:
            print("Successfully set gender")
        else:
            print("Error:", response.status_code, ":", response.text)

    def GetGender(self, ROBLOSECURITY):
        url = "https://users.roblox.com/v1/gender"

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
            "Referer": "https://users.roblox.com/v1/gender"
        })
        session.cookies[".ROBLOSECURITY"] = ROBLOSECURITY

        response = session.get(url)
        data = response.json()

        gender = data["gender"]

        if response.status_code == 200:
            if gender == 2:
                print("Male")
            elif gender == 3:
                print("Female")
            else:
                print("User is prefer not to say")
        else:
            print("Error:", response.status_code, ":", response.text)
    
    def SearchUsers(self, keyword):
        url = "https://users.roblox.com/v1/users/search"

        params = {}
        try:
            params['keyword'] = keyword
        except:
            print("Keyword is required")

        response = requests.get(url, params=params)
        data = response.json()
        users = data.get('data', [])

        number = 0
        for user in users:
            number += 1

            username = user.get('name')
            display_name = user.get('displayName')
            userID = user.get('id')

            print(number, ". Username:", username, ", Display name:", display_name, ", ID:", userID)



