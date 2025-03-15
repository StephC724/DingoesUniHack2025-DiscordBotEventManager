
#handles the point system
class pointSystem():
    pointDatabase = {"serverID": {"userID": {0}}}

    #called when points are added
    def userAddPoints(serverID: str, userID: str, points_amount: int): 
        pass
        # check if user already exists if they do add points if not add both

    #called at the start to rebuild from json file
    def unpackDatabase():
        pass

        #used to remove points from a user
    def userRemovePoints(serverID: str, userID: str, points_amount: int):
        pass

    #used to give a user a whole servers leaderboard
    def giveLeaderboard(serverID: str):
        pass

    #used to give a specific users points
    def giveUserPoints(serverID: str, userID str):
        pass

    #used to pack the databse into a JSON file for maintenience / downtime
    def packDatabase():
        pass

