
# create a class that will contain actions a dragon can take during combat
import json 
import config

class Actions():

    def __init__(self,dragonid):
        #open the dragon.json file and read the data
        #find the dragon with the dragonid
        #set the dragon's data to self
        with open(config.dragonjson, "r") as file:
            data = json.load(file)
            temp = data["dragons"]
            for i in temp:
                if i["id"] == dragonid:
                    self.dragon = i
                    break
            else:
                raise ValueError("Dragon not found")
        #check and see if the dragon is in an active combat challenge
        #if the dragon is in an active combat challenge, set the challengeid to self
        #if the dragon is not in an active combat challenge, raise an error
        with open(config.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challenger"]["dragonid"] == self.dragon["id"] or i["challengee"]["dragonid"] == self.dragon["id"]:
                    if i["status"] == "accepted":
                        self.challengeid = i["challengeid"]
                        break
            else:
                raise ValueError("Dragon not in an active challenge")            

        pass
    def move(self):
        # move the dragon to a new location in combat
        # current location is stored in the challenges.json file
        # valid locations are A, B, C, D, E
        # the dragon can move left or right
        # the dragon can move to the left if the dragon is not in the A column
        # the dragon can move to the right if the dragon is not in the E column
        # the dragon can move to the left or right if the dragon is in B, C or D columns


        #get current location from challenges.json file
        with open(config.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid:
                    if i["challenger"]["dragonid"] == self.dragon["id"]:
                        self.current_location = i["challenger"]["location"]
                    elif i["challengee"]["dragonid"] == self.dragon["id"]:
                        self.current_location = i["challengee"]["location"]
                        break
                    break
        
        # get the opponents location
        with open(config.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid:
                    if i["challenger"]["dragonid"] != self.dragon["id"]:
                        self.opponent_location = i["challenger"]["location"]
                    elif i["challengee"]["dragonid"] != self.dragon["id"]:
                        self.opponent_location = i["challengee"]["location"]
                        break
                    break

        # if the ownerid is cpu, the dragon will move towards the other dragon
        if self.dragon["ownerid"] == "cpu":
            # if the dragon is in the same column as the other dragon, the dragon will not move
            if self.current_location == self.opponent_location:
                pass
            # if the dragon is in a column to the left of the other dragon, the dragon will move right
            #convert the current location to a number
            if self.current_location == "A":
                self.current_location_int = 1
            elif self.current_location == "B":
                self.current_location_int = 2
            elif self.current_location == "C":
                self.current_location_int = 3
            elif self.current_location == "D":
                self.current_location_int = 4
            elif self.current_location == "E":
                self.current_location_int = 5
            #convert the opponent location to a number
            if self.opponent_location == "A":
                self.opponent_location_int = 1
            elif self.opponent_location == "B":
                self.opponent_location_int = 2
            elif self.opponent_location == "C":
                self.opponent_location_int = 3
            elif self.opponent_location == "D":
                self.opponent_location_int = 4
            elif self.opponent_location == "E":
                self.opponent_location_int = 5
            # if the dragon is in a column to the right of the other dragon, the dragon will move left
            # if the dragon is in a column to the left of the other dragon, the dragon will move right
            if self.opponent_location_int > self.current_location_int:
                self.current_location_int += 1
            elif self.opponent_location_int < self.current_location_int:
                self.current_location_int -= 1 
            #convert the current location back to a letter
            if self.current_location_int == 1:
                self.current_location = "A"
            elif self.current_location_int == 2:
                self.current_location = "B"
            elif self.current_location_int == 3:
                self.current_location = "C"
            elif self.current_location_int == 4:
                self.current_location = "D"
            elif self.current_location_int == 5:
                self.current_location = "E"
            #update the challenges.json file with the new location
            with open(config.challengesjson, "r") as file:
                data = json.load(file)
                temp = data["challenges"]
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        if i["challenger"]["dragonid"] == self.dragon["id"]:
                            i["challenger"]["location"] = self.current_location
                        elif i["challengee"]["dragonid"] == self.dragon["id"]:
                            i["challengee"]["location"] = self.current_location
                            break
                        break
            with open(config.challengesjson, "w") as file:
                json.dump(data, file, indent=4)
                
                   
        else:
            # if the ownerid is not cpu, the dragon will move based on user input
            # if the user enters a direction that is not valid, the dragon will not move

            # if the ownerid is cpu, the dragon will move towards the other dragon
            # if the dragon is in the same column as the other dragon, the dragon will not move
            # if the dragon is in a column to the left of the other dragon, the dragon will move right
            # if the dragon is in a column to the right of the other dragon, the dragon will move left
            pass









# test the Actions class
if __name__ == "__main__":
    test = Actions(47)
    print(test.dragon)
    test.move()