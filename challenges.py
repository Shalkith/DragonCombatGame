# create a challenge class that will allow for the creation of challenges between users in the json file
# this will allow for the creation of a challenge between two users, and the ability to accept or deny the challenge
# the challenge will be stored in the json file, and will be removed once the challenge is completed or denied
# consider the ownerid and the dragon id of the challenger and the challengee as a way to identify the challenge

import json
import random
import datetime
import config 
class Challenge:
    def __init__(self):
        self.challengesjson = config.challengesjson
        try:
            #use the config.py file to get the path to the json file
            with open(self.challengesjson, "r") as file:
                pass
        except:
            data = {"challenges": []}
            with open(self.challengesjson, "w") as file:
                json.dump(data, file, indent=4)
        pass

    def accept_challenge(self, challengeid):
        # read the challenges.json file and find the challenge with the challengeid
        # if the challenge is found, set the status to accepted
        # if the challenge is not found, raise an error
        with open(self.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == challengeid and i["status"] == "pending":
                    i["status"] = "accepted"
                    break
            else:
                raise ValueError("Challenge not found")
        with open(self.challengesjson, "w") as file:
            json.dump(data, file, indent=4)

    def initiate_challenge(self, challenger,challengee):
        #create an empty challenges.json file if it doesn't exist
        # if it does exist, read the file and append the challenge to the file
        
        self.challenger_ownerid = challenger["ownerid"]
        self.challenger_dragonid = challenger["id"]
        self.challengee_ownerid = challengee["ownerid"]
        self.challengee_dragonid = challengee["id"]
        # generate a challengeid that doesnt already exist in the json file
        with open(self.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            while True:
                self.challengeid = random.randint(100000, 999999)
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        continue
                    else:
                        break
                break
        # set the status of the challenge to pending
        self.status = "pending"
            
        self.challenge_completed_time = None
        # create a variable that will store the time the challenge was sent based on datetime.datetime.now()
        self.challenge_sent_time = datetime.datetime.now()

        # if challengee_ownerid is the same as challenger_ownerid, raise an error
        if self.challenger_dragonid == self.challengee_dragonid:
            raise ValueError("You can not challenge yourself")
        
        #if challengee_ownerid is cpu accept the challenge automatically
        if self.challengee_ownerid == "cpu":
            self.status = "accepted"

        # have a section for the challenger and the challengee
        self.challenge = {
            "challenger": {
                "dragonname": challenger["name"],
                "dragonid": self.challenger_dragonid,
                "latter_position": challenger["latter_position"],
                "ownerid": self.challenger_ownerid
            },
            "challengee": {
                "dragonname": challengee["name"],
                "dragonid": self.challengee_dragonid,
                "latter_position": challengee["latter_position"],
                "ownerid": self.challengee_ownerid,
            },
            "challengeid": self.challengeid,
            "status": self.status,
            "challenge_sent_time": self.challenge_sent_time.strftime("%m/%d/%Y, %H:%M:%S"),
            "challenge_completed_time": self.challenge_completed_time
        }
        self.challengejson = json.dumps(self.challenge)

        # write the challenge to the json file
        with open(self.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            temp.append(self.challenge)
            data["challenges"] = temp
        with open(self.challengesjson, "w") as file:
            json.dump(data, file, indent=4)





   

