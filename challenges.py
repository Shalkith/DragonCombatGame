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
        
        # set the location for both dragons to location A
        self.challenger_location = "A"
        self.challengee_location = "A"

        #set active_turn to false for both dragons intially
        self.challenger_active_turn = False
        self.challengee_active_turn = False

        #set challenge step to pending
        self.challenge_step = "pending"
        #set combat step to 0
        self.combat_step = 1
        # set status effects to an empty list for both dragons
        self.status_effects = []


        #set the starting life / max life for both dragons based on dragon.json
        # Also set combat dice - this is equal to speed divided by 10 rounded down plus 1

        

        with open(config.dragonjson, "r") as file:
            dragons = json.load(file)
            for i in dragons["dragons"]:
                if i["id"] == self.challenger_dragonid:
                    self.challenger_life = i["life"]
                    self.challenger_max_life = i["life"]
                    self.challenger_combat_dice = i["speed"] // 10 + 1
                    self.challenger_essence = i["essence"]
                    self.challenger_max_essence = i["essence"]
                    self.challenger_speed = i["speed"]
                    self.challenger_attack = i["attack"]
                    self.challenger_defense = i["defense"]
                    self.challenger_intellect = i["intellect"]
                    self.challenger_will = i["will"]
                    self.challenger_body = i["body"]
                    self.challenger_resist = i["resist"]
                    self.challenger_speed = i["speed"]
                    self.challenger_skills = i["skills"]
                    self.challenger_spells = i["spells"]
                    self.challenger_abilities = i["abilities"]

                    
                elif i["id"] == self.challengee_dragonid:
                    self.challengee_life = i["life"]
                    self.challengee_max_life = i["life"]
                    self.challengee_combat_dice = i["speed"] // 10 + 1
                    self.challengee_essence = i["essence"]
                    self.challengee_max_essence = i["essence"]
                    self.challengee_speed = i["speed"]
                    self.challengee_attack = i["attack"]
                    self.challengee_defense = i["defense"]
                    self.challengee_intellect = i["intellect"]
                    self.challengee_will = i["will"]
                    self.challengee_body = i["body"]
                    self.challengee_resist = i["resist"]
                    self.challengee_skills = i["skills"]
                    self.challengee_spells = i["spells"]
                    self.challengee_abilities = i["abilities"]









        # have a section for the challenger and the challengee
        self.challenge = {
            "challengeid": self.challengeid,
            "status": self.status,
            "challenge_sent_time": self.challenge_sent_time.strftime("%m/%d/%Y, %H:%M:%S"),
            "challenge_completed_time": self.challenge_completed_time,
            "challenge_step": self.challenge_step,
            "combat_step": self.combat_step,
            "challenger": {
                "dragonname": challenger["name"],
                "id": self.challenger_dragonid,
                "latter_position": challenger["latter_position"],
                "ownerid": self.challenger_ownerid,
                "location": self.challenger_location,
                "life": self.challenger_life,
                "max_life": self.challenger_max_life,
                "essence": self.challenger_essence,
                "max_essence": self.challenger_max_essence,
                "active_turn": self.challenger_active_turn,
                "status_effects": self.status_effects,
                "combat_dice": self.challenger_combat_dice,
                "speed": self.challenger_speed,
                "attack": self.challenger_attack,
                "defense": self.challenger_defense,
                "intellect": self.challenger_intellect,
                "will": self.challenger_will,
                "body": self.challenger_body,
                "resist": self.challenger_resist,
                "skills": self.challenger_skills,
                "spells": self.challenger_spells,
                "abilities": self.challenger_abilities
            },
            "challengee": {
                "dragonname": challengee["name"],
                "id": self.challengee_dragonid,
                "latter_position": challengee["latter_position"],
                "ownerid": self.challengee_ownerid,
                "location": self.challengee_location,
                "life": self.challengee_life,
                "max_life": self.challengee_max_life,
                "essence": self.challengee_essence,
                "max_essence": self.challengee_max_essence,
                "active_turn": self.challengee_active_turn,
                "status_effects": self.status_effects,
                "combat_dice": self.challengee_combat_dice,
                "speed": self.challengee_speed,
                "attack": self.challengee_attack,
                "defense": self.challengee_defense,
                "intellect": self.challengee_intellect,
                "will": self.challengee_will,
                "body": self.challengee_body,
                "resist": self.challengee_resist,
                "skills": self.challengee_skills,
                "spells": self.challengee_spells,
                "abilities": self.challengee_abilities


            }

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





   

