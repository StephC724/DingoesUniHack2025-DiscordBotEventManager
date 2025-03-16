import json

sampleJson = '{"serverID": {"userID": {0}}'


#handles the point system
class pointSystem():

    serversKey = "Servers"
    usersKey = "Users"
    pointsKey = "UserPoints" # Set a customizable key for the points

    def __init__(self):

        # self.pointDatabase = {"serverID": {"userID": {self.pointsKey: 0}}} # Here for now we've assumed the json has been accessed and converted to a dictionary already
        self.pointDatabase = {self.serversKey:{"serverID":{self.usersKey:{"userID":{self.pointsKey:0}}}}}


    #called at the start to rebuild from json file
    def unpackDatabase(self,fileName):
        with open(fileName,"r") as json_file:
            textData = json.load(json_file)
            # For some reason json.loads(json_file) causes TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper

        convertedToDict = json.loads(textData)

        self.pointDatabase = convertedToDict

    def getAllServerKeys(self,database):
        return database[self.serversKey].keys()
    
    def getServerUsers(self,database,serverID):
        return database[self.serversKey][serverID][self.usersKey].keys()
        
    #Gets user points, This stuff
    def getUserPoints(self, serverID: str, userID: str):
    """Retrieves the points of a user from a specific server."""
    if self.checkServerExists(serverID):
        if self.checkUserExists(serverID, userID):
            # Return the user's points
            return self.pointDatabase[self.serversKey][serverID][self.usersKey][userID][self.pointsKey]
        else:
            print("\n-------------------------------------------------------------------------------------\nUSER DOESN'T EXISTS\n-------------------------------------------------------------------------------------\n")
            return None
    else:
        print("\n-------------------------------------------------------------------------------------\nSERVER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
        return None

    
    #called when points are added
    def userAddPoints(self, serverID: str, userID: str, points_amount: int): 
        if self.checkServerExists(serverID):
            print("\n-------------------------------------------------------------------------------------\nSERVER EXISTS\n-------------------------------------------------------------------------------------\n")
            chosenServer = self.pointDatabase[self.serversKey][serverID]
            if self.checkUserExists(serverID,userID):
                print("\n-------------------------------------------------------------------------------------\nUSER EXISTS\n-------------------------------------------------------------------------------------\n")
            else:
                print("\n-------------------------------------------------------------------------------------\nUSER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
                # Use addNewUser
                self.addNewUser(serverID,userID)
        else:
            print("\n-------------------------------------------------------------------------------------\nSERVER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
            # Use addNewServer
            self.addNewServer(serverID)
            self.addNewUser(serverID,userID)
        # check if user already exists if they do add points if not add both

        self.pointDatabase[self.serversKey][serverID][self.usersKey][userID][self.pointsKey] += points_amount
    

        #used to remove points from a user
    def userRemovePoints(self,serverID: str, userID: str, points_amount: int):
        if self.checkServerExists(serverID):
            print("\n-------------------------------------------------------------------------------------\nSERVER EXISTS\n-------------------------------------------------------------------------------------\n")
            chosenServer = self.pointDatabase[self.serversKey][serverID]
            if self.checkUserExists(serverID,userID):
                print("\n-------------------------------------------------------------------------------------\nUSER EXISTS\n-------------------------------------------------------------------------------------\n")
            else:
                print("\n-------------------------------------------------------------------------------------\nUSER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
                # Use addNewUser
                self.addNewUser(serverID,userID)
        else:
            print("\n-------------------------------------------------------------------------------------\nSERVER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
            # Use addNewServer
            self.addNewServer(serverID)
            self.addNewUser(serverID,userID)
        # check if user already exists if they do add points if not add both

        usersPoints = self.pointDatabase[self.serversKey][serverID][self.usersKey][userID][self.pointsKey]
        usersPoints -= points_amount
        if (usersPoints - points_amount) < 0:
            usersPoints = 0


    #used to give a user a whole servers leaderboard
    def giveLeaderboard(self,serverID: str):
        pass

    #used to set a user to a specified amount of points
    def giveUserPoints(self,serverID: str, userID: str, points_amount: int):
        if self.checkServerExists(serverID):
            print("\n-------------------------------------------------------------------------------------\nSERVER EXISTS\n-------------------------------------------------------------------------------------\n")
            chosenServer = self.pointDatabase[self.serversKey][serverID]
            if self.checkUserExists(serverID,userID):
                print("\n-------------------------------------------------------------------------------------\nUSER EXISTS\n-------------------------------------------------------------------------------------\n")
            else:
                print("\n-------------------------------------------------------------------------------------\nUSER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
                # Use addNewUser
                self.addNewUser(serverID,userID)
        else:
            print("\n-------------------------------------------------------------------------------------\nSERVER DOESN'T EXIST\n-------------------------------------------------------------------------------------\n")
            # Use addNewServer
            self.addNewServer(serverID)
            self.addNewUser(serverID,userID)
        # check if user already exists if they do add points if not add both

        self.pointDatabase[self.serversKey][serverID][self.usersKey][userID][self.pointsKey] = points_amount

    def addNewServer(self,serverID: str):
        self.pointDatabase[self.serversKey][serverID] = {}
        self.pointDatabase[self.serversKey][serverID][self.usersKey] = {}
    
    def addNewUser(self,serverID: str,userID: str):
        self.pointDatabase[self.serversKey][serverID][self.usersKey][userID] = {self.pointsKey: 0}

    def checkServerExists(self,serverID: str):
        # print(self.pointDatabase[serverID] is not None,"JSKDLF:JKSDJF:LKSJDF:LSDJKFSDFGHJKLKHSID:JFIKJSDJF:SJDFSEKJFO:JSIDKLJFHEISKFJ")
        # return self.pointDatabase[serverID] is not None
        print("JLSKDFJS:LDKFLS:DJFKLSDFD",self.pointDatabase,"JSKLDFJ:SDJFKLSDJ:FKJSD:FLKD")
        print(self.pointDatabase.keys())
        print(serverID in self.pointDatabase[self.serversKey].keys())
        return serverID in self.pointDatabase[self.serversKey].keys()
    
    def checkUserExists(self,serverID: str, userID: str):
        return userID in self.pointDatabase[self.serversKey][serverID][self.usersKey].keys()

    #used to pack the databse into a JSON file for maintenience / downtime
    def packDatabase(self):
        convertedToJson = json.dumps(self.pointDatabase)

        with open("data.json", "w") as file:
            json.dump(convertedToJson, file)
