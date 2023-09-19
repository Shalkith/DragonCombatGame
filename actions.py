
# create a class that will contain actions a dragon can take during combat
import json 
import config
import random

class Actions():

    def __init__(self,dragon):
        dragonid = dragon["id"]
        
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
        
        roll,roll_log = self.roll_dice(dice=attacker["combat_dice"],bonusdice=attacker["attack_die_bonus"],adjustment=attacker["roll_adjustment"],dragon=attacker) 
        if config.debug == True:
            print()
            print(
                "Attacker: ",attacker["name"], "is using ",move,". Against ",defender["name"])
            print(roll_log)
        attackerresult += roll
        # if the movetype is a skill, the attacker add its attack value to the result
        if movetype == "skill":
            attackerresult += attacker["attack"]
            if config.debug == True:
                print("Attack value: ",attacker["attack"])
        
        # if the movetype is a spell, the attacker add its intellect value to the result
        elif movetype == "spell":
            attackerresult += attacker["intellect"]
            if config.debug == True:
                print("Intellect value: ",attacker["intellect"])
        if config.debug == True:
            print(attacker["name"], "rolled: ",attackerresult)
        



        # defender rolls its combat dice:
        # roll a d6 equal to number of dice
        defenderresult = 0
        temp_defense_die_bonus =  defender["defense_die_bonus"]
        if defender["rested_bonus"] == True:
            defender["rested_bonus"] = False
            temp_defense_die_bonus = defender["combat_dice"] + 1
            if config.debug == True:
                print(defender["name"], "is rested and gets a bonus die")
        roll,roll_log = self.roll_dice(dice=defender["combat_dice"],bonusdice=temp_defense_die_bonus,adjustment=defender["roll_adjustment"],dragon=defender)
        if config.debug == True:
            print(
                "Defender: ",defender["name"], "is defending against ",attacker["name"],"'s ",move)
            print(roll_log)
            print()
        defenderresult += roll
                
        # if the movetype is a skill, the defender add its defense value to the result
        if movetype == "skill":
            defenderresult += defender["defense"]
            if config.debug == True:
                print("Defense value: ",defender["defense"])
        # if the movetype is a spell, the defender add its will value to the result
        elif movetype == "spell":
            defenderresult += defender["will"]
            if config.debug == True:
                print("Will value: ",defender["will"])
        if config.debug == True:
            print(defender["name"], "rolled: ",defenderresult)

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
            damage,roll_log = self.roll_dice(dice,0,attacker["roll_adjustment"],self.dragon)
            #add the bonus
            max_damage = damage + bonus
            
        
        else:
            result = "unsuccessful"
            max_damage = 0
            cost = cost//2
            if cost < 1:
                cost = 1
        return result,max_damage,cost,roll_log

    def roll_dice(self,dice,bonusdice,adjustment,dragon):
        rule_of_6 = 0
        rolls = []
        damage = 0
        roll_log = ''
        roll_log += dragon["name"] + " is rolling " + str(dice) + " dice, " + str(bonusdice) + " bonus dice and has a " + str(adjustment) + " point adjustment "

        total_dice = dice + bonusdice   
        for r in range(total_dice):
            roll = random.randint(1,6)
            if roll == 6:
                rule_of_6 += 1
            if roll == 1:
                rule_of_6 -= 1
            rolls.append(roll)
            damage += roll
            roll_log += "Rolled: "+ str(roll) + " "
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
            roll_log += "Rule of 6 rolls: " + str(rolls) + " "
        #add the adjustment
        damage += adjustment
        roll_log += str(damage) + " points of damage after adjustment"

        
        return damage,roll_log
          

# test the Actions class
if __name__ == "__main__":
    #select a random dragon from the dragon.json file
    with open(config.dragonjson, "r") as file:
        data = json.load(file)
        temp = data["dragons"]
        for dragon in temp:
            if dragon["id"] == 2:
                randdragon = random.choice(temp)
                dragon = dragon
                break
    test = Actions(dragon)
    #print(test.dragon)
    damage,roll_log = test.roll_dice(1,15,1,dragon)
    print(roll_log)