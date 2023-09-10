# create a class to handle combat between dragons
import json 
import random
import datetime

class Combat:
    def __init__(self, challengeid):
        self.challengeid = challengeid
        #retrieve the challenge from the challenges.json file
        with open("challenges.json", "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid and i["status"] == "accepted":
                    self.challenge = i
                    break
            else:
                raise ValueError("Challenge not found or not accepted")
        #retrieve the challenger and challengee from the dragons.json file
        with open("dragon.json", "r") as file:
            data = json.load(file)
            temp = data["dragons"]
            for i in temp:
                if i["ownerid"] == self.challenge["challenger"]["ownerid"] and i["id"] == self.challenge["challenger"]["dragonid"]:
                    self.challenger = i
                elif i["ownerid"] == self.challenge["challengee"]["ownerid"] and i["id"] == self.challenge["challengee"]["dragonid"]:
                    self.challengee = i
        
    def log_combat(self):
        # create a combat log file if it doesn't exist
        # if it does exist, append the combat to the file
        # the combat log should include the winner, loser, and the time the combat was completed
        # The combat log should also include the challengeid, and latter_position of the winner and loser before and after combat
        try :
            with open("combat_log.json", "r") as file:
                pass
        except:
            data = {"combat_log": []}
            with open("combat_log.json", "w") as file:
                json.dump(data, file, indent=4)
        with open("combat_log.json", "r") as file:
            data = json.load(file)
            temp = data["combat_log"]
            #append challengeid,time complete and winner object and a loser object, each containing name, id,latter_position, ownerid
            temp.append({"challengeid": self.challengeid, "time_completed": str(self.challenge["challenge_completed_time"]), "winner": {"name": self.winner["name"], "id": self.winner["id"], "latter_position": self.winner["latter_position"], "ownerid": self.winner["ownerid"]}, "loser": {"name": self.loser["name"], "id": self.loser["id"], "latter_position": self.loser["latter_position"], "ownerid": self.loser["ownerid"]}})
            
        with open("combat_log.json", "w") as file:
            json.dump(data, file, indent=4)
        
        # update challenge.json to compelte

        with open("challenges.json", "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid:
                    i["status"] = "completed"
                    break
        with open("challenges.json", "w") as file:
            json.dump(data, file, indent=4)
        




    def start_combat(self):
        self.winner = random.choice([self.challenger, self.challengee])
        if self.winner == self.challenger:
            self.loser = self.challengee
        else:
            self.loser = self.challenger
        self.finish_combat()
        return self.winner, self.loser
        # determine the winner and loser of the combat
        # set the status of the challenge to completed
        # set the winner and loser of the challenge
        # set the time the challenge was completed
        # save the changes to the challenges.json file
        # save the changes to the dragon.json file
        # return the winner and loser of the combat
    def finish_combat(self):

        self.challenge["status"] = "completed"
        self.challenge["winner"] = self.winner["ownerid"]
        self.challenge["loser"] = self.loser["ownerid"]
        self.challenge["challenge_completed_time"] = datetime.datetime.now()
        with open("challenges.json", "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid:
                    i = self.challenge
                    break
        with open("challenges.json", "w") as file:
            json.dump(data, file, indent=4)
        with open("dragon.json", "r") as file:
            data = json.load(file)
            temp = data["dragons"]
            for i in temp:
                if i["ownerid"] == self.winner["ownerid"] and i["id"] == self.winner["id"]:
                    i["wins"] += 1
                    if self.winner["latter_position"] > self.loser["latter_position"]:
                        i["latter_position"] = self.loser["latter_position"]

                elif i["ownerid"] == self.loser["ownerid"] and i["id"] == self.loser["id"]:
                    i["losses"] += 1
                    if self.loser["latter_position"] < self.winner["latter_position"]:
                        i["latter_position"] = self.winner["latter_position"]

        with open("dragon.json", "w") as file:
            json.dump(data, file, indent=4)
        # pull the winner and loser from the dragon.json file
        with open("dragon.json", "r") as file:
            data = json.load(file)
            temp = data["dragons"]
            for i in temp:
                if i["ownerid"] == self.winner["ownerid"] and i["id"] == self.winner["id"]:
                    self.winner = i
                elif i["ownerid"] == self.loser["ownerid"] and i["id"] == self.loser["id"]:
                    self.loser = i
                     
        
        self.log_combat()
        return self.winner, self.loser
    
    

if __name__ == "__main__":
    # test combat class
    c = Combat(184776)
    print()
    #print(c.challenge)
    print(c.challenger)
    print()
    print(c.challengee)
    print()
    print()
    print()
    winner, loser = c.start_combat()
    print(winner)
    print()
    print(loser)



        
