import requests
from timeconverter import *
from numbershorter import *

class GroupData:
    def __init__(self, groupID, memberCount=0, name=None, owner=None, created=0, updated=0):
        self.groupID = groupID  # Group ID
        self.memberCount = memberCount  # How many members are in the group
        self.name = name  # Gets name of the group
        self.owner = owner  # Gets name of the owner
        self.created = created  # Date of creating the group
        self.updated = updated  # Date of the last updating of the group

class Groups:
    def __init__(self):
        self.groups = {}  # Stores the group data

    def FindDataAboutGroup(self, groupID):
        api_url = f"https://groups.roblox.com/v1/groups/{groupID}"

        if groupID not in self.groups:
            self.groups[groupID] = GroupData(groupID)

        try:  # Trying to get the data, if it didn't, it prints an error
            response = requests.get(api_url)  # Sends request to the URL, then returns the result
            response.raise_for_status()

            data = response.json()  # Converts data to JSON
        
            name = data["name"]
            self.groups[groupID].name = name         
            memberCount = data["memberCount"]
            memberCount = shorter_number(memberCount)
            self.groups[groupID].memberCount = memberCount
            owner = data["owner"]["username"]
            self.groups[groupID].owner = owner
            created = data["created"]
            created = ConvertTimestamp(created)
            self.groups[groupID].created = created
            updated = data["updated"]
            updated = ConvertTimestamp(updated)
            self.groups[groupID].updated = updated

        except requests.exceptions.RequestException as error:  # If an error while getting data has occurred (most likely don't have access, or invalid URL)
            print("Request error:", error)

        return self.groups[groupID]
    
