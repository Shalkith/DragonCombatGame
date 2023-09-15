
# create a class that will contain actions a dragon can take during combat
import json 
import config
import random

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
                if i["challenger"]["id"] == self.dragon["id"] or i["challengee"]["id"] == self.dragon["id"]:
                    if i["status"] == "accepted":
                        self.challengeid = i["challengeid"]
                        break
            else:
                raise ValueError("Dragon not in an active challenge")            

        pass
    def move(self,current_location,opponent_location):

        # move the dragon to a new location in combat
        # current location is stored in the challenges.json file
        # valid locations are A, B, C, D, E
        # the dragon can move left or right
        # the dragon can move to the left if the dragon is not in the A column
        # the dragon can move to the right if the dragon is not in the E column
        # the dragon can move to the left or right if the dragon is in B, C or D columns
        self.current_location = current_location
        self.opponent_location = opponent_location

        if config.debug == True:
            print("Current location: ", self.current_location)
            print("Opponent location: ", self.opponent_location)


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

            if config.debug == True:
                print("New location: ", self.current_location)
            
            return self.current_location
                
                   
        else:
            # if the ownerid is not cpu, the dragon will move based on user input
            # if the user enters a direction that is not valid, the dragon will not move

            # if the ownerid is cpu, the dragon will move towards the other dragon
            # if the dragon is in the same column as the other dragon, the dragon will not move
            # if the dragon is in a column to the left of the other dragon, the dragon will move right
            # if the dragon is in a column to the right of the other dragon, the dragon will move left
            pass
    def use(self,movetype,move,cost,attacker,defender):

        #get the attacker breed from dragon.json

        with open(config.dragonjson, "r") as file:
            data = json.load(file)
            temp = data["dragons"]
            for i in temp:
                if i["id"] == attacker["id"]:
                    attackerbreed = i["breed"]
                    break
            else:
                raise ValueError("Dragon not found")


        # attacker rolls its combat dice:
        # roll a d6 equal to number of dice
        attackerresult = 0 
        for r in range(attacker["combat_dice"]):
            attackerresult += random.randint(1,6)
        # defender rolls its combat dice:
        # roll a d6 equal to number of dice
        defenderresult = 0
        for r in range(defender["combat_dice"]):
            defenderresult += random.randint(1,6)
        
        # if the movetype is a skill, the attacker add its attack value to the result
        # if the movetype is a skill, the defender add its defense value to the result
        if movetype == "skill":
            attackerresult += attacker["attack"]
            defenderresult += defender["defense"]
        # if the movetype is a spell, the attacker add its intellect value to the result
        # if the movetype is a spell, the defender add its will value to the result
        elif movetype == "spell":
            attackerresult += attacker["intellect"]
            defenderresult += defender["will"]

        # if the attackerresult is greater than the defenderresult, the attack is successful
        # if the attackerresult is less than the defenderresult, the attack is unsuccessful
        # if the attackerresult is equal to the defenderresult, the attack is unsuccessful
        if attackerresult > defenderresult:
            result = "successful"
            max_damage = 0
            #get the rating for the moved used from attacker object
            if movetype == "skill":
                rating = attacker["skills"][move]
            elif movetype == "spell":
                rating = attacker["spells"][move]

            #get the damage code from the config.breed_abilities

            # get attackers skill or spell rating based on movetype and move
            rating = attacker[movetype][move]
            #             
            damage_code = config.breed_abilities[attackerbreed][movetype][move]["damage_code"]
            if config.debug == True:
                print("Damage code: ",damage_code)
                print("Rating: ",rating)

            #get the damagechart from damage_chart.json
            #get  dice and bonus from damagechart
            with open(config.damagechartjson, "r") as file:
                data = json.load(file)
                temprating = rating
                if temprating > 20:
                    temprating = 20
                dice = data[damage_code][str(rating)]["dice"]
                bonus = data[damage_code][str(rating)]["bonus"]

            #roll the dice            
            damage = self.roll_dice(dice)
            #add the bonus
            max_damage = damage + bonus
            
        
        else:
            result = "unsuccessful"
            max_damage = 0
            cost = cost//2
            if cost < 1:
                cost = 1
        return result,max_damage,cost

    def roll_dice(self,dice):
        rule_of_6 = 0
        rolls = []
        damage = 0

        for r in range(dice):
            roll = random.randint(1,6)
            if roll == 6:
                rule_of_6 += 1
            if roll == 1:
                rule_of_6 -= 1
            rolls.append(roll)
            damage += roll
        if config.debug == True:
            print("Rolled: ",rolls)
        #if the rule of 6 is greater than 0, roll the dice again for each number above zero
        while rule_of_6 > 0:
            rolls = []
            rerolls = rule_of_6 
            rule_of_6 = 0
            for r in range(rerolls):
                roll = random.randint(1,6)
                rolls.append(roll)
                if roll == 6:
                    rule_of_6 += 1
                if roll == 1:
                    rule_of_6 -= 1
                damage += roll
            if config.debug == True:    
                print("Rule of 6 rolls: ",rolls)
        return damage
          








# test the Actions class
if __name__ == "__main__":
    test = Actions(74)
    print(test.dragon)
    test.roll_dice(1)