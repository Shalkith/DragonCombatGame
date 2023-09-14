# create a class to handle combat between dragons
import json 
import random
import datetime
import config 
import actions


class Combat:
    def __init__(self, challengeid):
        self.challengesjson = config.challengesjson
        self.dragonjson = config.dragonjson
        self.combatlogjson = config.combatlogjson


        self.challengeid = challengeid
        #retrieve the challenge from the challenges.json file
        with open(self.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid and i["status"] == "accepted":
                    self.challenge = i
                    break
            else:
                raise ValueError("Challenge not found or not accepted")
        #retrieve the challenger and challengee from the dragons.json file
        with open(self.dragonjson, "r") as file:
            data = json.load(file)
            temp = data["dragons"]
            for i in temp:
                if i["ownerid"] == self.challenge["challenger"]["ownerid"] and i["id"] == self.challenge["challenger"]["id"]:
                    self.challenger = i
                elif i["ownerid"] == self.challenge["challengee"]["ownerid"] and i["id"] == self.challenge["challengee"]["id"]:
                    self.challengee = i

        self.challenger = self.challenge["challenger"]
        self.challengee = self.challenge["challengee"]
    def log_combat(self):
        # create a combat log file if it doesn't exist
        # if it does exist, append the combat to the file
        # the combat log should include the winner, loser, and the time the combat was completed
        # The combat log should also include the challengeid, and latter_position of the winner and loser before and after combat
        try :
            with open(self.combatlogjson, "r") as file:
                pass
        except:
            data = {"combat_log": []}
            with open(self.combatlogjson, "w") as file:
                json.dump(data, file, indent=4)
        with open(self.combatlogjson, "r") as file:
            data = json.load(file)
            temp = data["combat_log"]
            #append challengeid,time complete and winner object and a loser object, each containing name, id,latter_position, ownerid, and if the dragnon is the challenger or challengee
            temp.append({"challengeid": self.challengeid, "time_completed": self.challenge["challenge_completed_time"], 
                         "winner": {"name": self.winner["name"], "id": self.winner["id"], "latter_position": self.winner["latter_position"], "ownerid": self.winner["ownerid"], "challenger": self.winner['id'] == self.challenger['id'], "challengee": self.winner['id'] == self.challengee['id']}, 
                         "loser": {"name": self.loser["name"], "id": self.loser["id"], "latter_position": self.loser["latter_position"], "ownerid": self.loser["ownerid"], "challenger": self.loser['id'] == self.challenger['id'], "challengee": self.loser['id'] == self.challengee['id']}})
            
        with open(self.combatlogjson, "w") as file:
            json.dump(data, file, indent=4)
        
        # update challenge.json to compelte and set the winner and loser

        with open(self.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid:
                    i["status"] = "completed"
                    i["winnerid"] = self.winner["id"]
                    i["winnername"] = self.winner["name"]
                    i["loserid"] = self.loser["id"]
                    i["losername"] = self.loser["name"]
                    i["challenge_completed_time"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                    break
        with open(self.challengesjson, "w") as file:
            json.dump(data, file, indent=4)


    def combat_round(self):
        # comban turns have 7 steps
        # 1. regain essence
        # 2. roll for random events
        # 3. roll for initiative (speed) 
        # 4 range (movement)
        # 5. dragon announces intent
        # 6. dragon rolls to see if a hit is scored
        # 7. damage resolution
        # 8. repeat steps 5-7 for each dragon
        # Restart this from step 1 until one dragon is dead

        # step 1. regain essence - if combat step is 1, regain 1 essence
        # do not exceed max essence
        if self.challenge["combat_step"] == 1:
            if config.debug:
                print("step 1")
            if self.challenger["essence"] < self.challenger["max_essence"]:
                self.challenger["essence"] += 1
            if self.challengee["essence"] < self.challengee["max_essence"]:
                self.challengee["essence"] += 1
            #set the combat step to 2\
            self.challenge["combat_step"] = 2
            # update the challengae json file to reflect the new essence values and the new combat step
            with open(self.challengesjson, "r") as file:
                data = json.load(file)
                temp = data["challenges"]
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        i["combat_step"] = self.challenge["combat_step"]
                        i["challenger"]["essence"] = self.challenger["essence"]
                        i["challengee"]["essence"] = self.challengee["essence"]
                        break

            with open(self.challengesjson, "w") as file:
                json.dump(data, file, indent=4)





            
            

        # step 2. roll for random events - if combat step is 2, roll for random events
        elif self.challenge["combat_step"] == 2:
            if config.debug:
                print("step 2")

            # each dragon must roll a 6 sided die
            challenger_roll = random.randint(1,6)
            challengee_roll = random.randint(1,6)
            # if the roll is a 1, a random event occurs, roll a 6 sided die to determine the event
            # events are as follows:
            # 1. Attacked by slayers
            # 2. Wrath of Gaia
            # 3. The call of Shalkith
            # 4. Breath of Gaia
            # 5. Wisdom of the Ancients
            # 6. The Sage Towers
            # add these events to the dragons status effects
            if challenger_roll == 1:
                event = random.randint(1,6)
                if event == 1:
                    self.challenger["status_effects"].append("Attacked by slayers")
                elif event == 2:
                    self.challenger["status_effects"].append("Wrath of Gaia")
                elif event == 3:
                    self.challenger["status_effects"].append("The call of Shalkith")
                elif event == 4:
                    self.challenger["status_effects"].append("Breath of Gaia")
                elif event == 5:
                    self.challenger["status_effects"].append("Wisdom of the Ancients")
                elif event == 6:
                    self.challenger["status_effects"].append("The Sage Towers")
            if challengee_roll == 1:
                event = random.randint(1,6)
                if event == 1:
                    self.challengee["status_effects"].append("Attacked by slayers")
                elif event == 2:
                    self.challengee["status_effects"].append("Wrath of Gaia")
                elif event == 3:
                    self.challengee["status_effects"].append("The call of Shalkith")
                elif event == 4:
                    self.challengee["status_effects"].append("Breath of Gaia")
                elif event == 5:
                    self.challengee["status_effects"].append("Wisdom of the Ancients")
                elif event == 6:
                    self.challengee["status_effects"].append("The Sage Towers")


            # set the combat step to 3
            self.challenge["combat_step"] = 3

            # update the challengae json file to reflect the new status effects and the new combat step
            with open(self.challengesjson, "r") as file:
                data = json.load(file)
                temp = data["challenges"]
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        i["combat_step"] = self.challenge["combat_step"]
                        i["challenger"]["status_effects"] = self.challenger["status_effects"]
                        i["challengee"]["status_effects"] = self.challengee["status_effects"]
                        break

            with open(self.challengesjson, "w") as file:
                json.dump(data, file, indent=4)


        # step 3. roll for initiative (speed) and range (movement) - if combat step is 3, roll for initiative and range
        elif self.challenge["combat_step"] == 3:
            if config.debug:
                print("step 3")

            #each dragon rolls a 6 sided die and adds their speed to the roll
            # the dragon with the higher roll goes first if there is a tie, use speed rating, if theres a tie roll again
            # set the active turn to the dragon with the higher roll in the challenge.json
            challenger_roll, challengee_roll = 0,0
            while challenger_roll == challengee_roll:

                challenger_roll = random.randint(1,6) + self.challenger["speed"]
                challengee_roll = random.randint(1,6) + self.challengee["speed"]
                if config.debug:
                    print("challenger roll: " + str(challenger_roll))
                    print("challengee roll: " + str(challengee_roll))
                if challenger_roll > challengee_roll:
                    self.challenger["active_turn"] = True
                    self.challengee["active_turn"] = False
                elif challengee_roll > challenger_roll:
                    self.challenger["active_turn"] = False
                    self.challengee["active_turn"] = True
                elif self.challenge["speed"] > self.challengee["speed"]:
                    self.challenger["active_turn"] = True
                    self.challengee["active_turn"] = False
                elif self.challengee["speed"] > self.challenger["speed"]:
                    self.challenger["active_turn"] = False
                    self.challengee["active_turn"] = True
                else:
                    raise ValueError("Speed is equal and a tie can not be broken")
            # set the combat step to 4
            self.challenge["combat_step"] = 4                   
            # update the challengae json file to reflect the new active turn and the new combat step
            with open(self.challengesjson, "r") as file:
                data = json.load(file)
                temp = data["challenges"]
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        i["combat_step"] = self.challenge["combat_step"]
                        i["challenger"]["active_turn"] = self.challenger["active_turn"]
                        i["challengee"]["active_turn"] = self.challengee["active_turn"]
                        break

            with open(self.challengesjson, "w") as file:
                json.dump(data, file, indent=4)

                
        # step 4 range (movement) - if combat step is 4, roll for range
        elif self.challenge["combat_step"] == 4:
            if config.debug:
                print("step 4")

            # for each dragon in the challenge, determin how many spaces they can move
            # a dragon can move 1 space plus one space for every 10 points of speed rounded down
            # the dragon who's actice_turn is true will move last
            # update the challenge json file with the new location of the dragons
            # for each dragon in the challenge 
            self.challenger_actions = actions.Actions(self.challenger["id"])
            self.challengee_actions = actions.Actions(self.challengee["id"])

            if self.challengee["active_turn"]:
                moves = self.challenger["speed"] // 10 +1
                print('challenger moves',moves)
                for i in range(moves):
                    self.challenger["location"] = self.challenger_actions.move(self.challenger["location"], self.challengee["location"])
                moves = self.challengee["speed"] // 10+1
                print('challengee moves',moves)
                for i in range(moves):
                    self.challengee["location"] = self.challengee_actions.move(self.challengee["location"], self.challenger["location"])
            elif self.challenger["active_turn"]:
                moves = self.challengee["speed"] // 10+1
                for i in range(moves):
                    self.challengee["location"] = self.challengee_actions.move(self.challengee["location"], self.challenger["location"])   
                moves = self.challenger["speed"] // 10+1
                for i in range(moves):
                    self.challenger["location"] = self.challenger_actions.move(self.challenger["location"], self.challengee["location"])
            
            # set the combat step to 5            
            self.challenge["combat_step"] = 5
            print(self.challenger["location"],self.challengee["location"])
            # update the challengae json file to reflect the new location of the dragons and the new combat step
            with open(self.challengesjson, "r") as file:
                data = json.load(file)
                temp = data["challenges"]
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        i["combat_step"] = self.challenge["combat_step"]
                        i["challenger"]["location"] = self.challenger["location"]
                        i["challengee"]["location"] = self.challengee["location"]
                        break

            with open(self.challengesjson, "w") as file:
                json.dump(data, file, indent=4)



            
        # steps 5 6 and 7 are repeated for each dragon in the challenge
        # check to see if the challenger or challengee is dead before passing to the next dragon- if so, end combat
        # step 5. dragon announces intent - if combat step is 5, the dragon announces intent
        elif self.challenge["combat_step"] == 5:
            if config.debug:
                print("step 5")
            # the dragon who's active_turn is true announces intent
            # for now dragons will only attack with claw attack 
            
            
            if self.challenger["active_turn"]:
                #pick a random skill spell or ability from self.challenger["skills"] or self.challenger["spells"] or self.challenger["abilities"]
                #if the dragon has enough essence, use the skill spell or ability
                #if the dragon does not have enough essence, use claw attack
                #if the dragon has enough essence, use the skill spell or ability
                choice = random.choice(self.challenger["skills"] + self.challenger["spells"] + self.challenger["abilities"])
                # lookup the chosen skill spell or ability in the config file and get its essense_used value

                for ability in config.breed_abilities:
                    if ability == choice["Name"]:
                        cost = config.breed_abilities[ability]["essence_used"]
                        break

                if cost <= self.challenger["essence"]:
                    #self.challenger_actions.use(choice["Name"], self.challengee["dragonid"])
                    print("use ability"+choice)
                else:
                    choice = self.challenger["skills"]["claw_attack"]










                self.challenger_actions.attack(self.challengee["dragonid"])
            elif self.challengee["active_turn"]:
                self.challengee_actions.attack(self.challenger["dragonid"])
            # set the combat step to 6
            self.challenge["combat_step"] = 6
            # update the challengae json file to reflect the new combat step
            

        # step 6. dragon rolls to see if a hit is scored - if combat step is 6, roll to see if a hit is scored
        elif self.challenge["combat_step"] == 6:
            if config.debug:
                print("step 6")


            

            #set the combat step to 6
            self.challenge["combat_step"] = 6
            #self.update_challenge(self)

        # step 6. dragon rolls to see if a hit is scored - if combat step is 6, roll to see if a hit is scored

        # step 7. damage resolution - if combat step is 7, resolve damage
        elif self.challenge["combat_step"] == 7:
            if config.debug:
                print("step 7")


            #set the combat step to 1
            #self.challenge["combat_step"] = 1
            #update the challenge json 
            
        print('updating') 
        self.update_challenge()
        














            



        

                
                
            


            
                



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
        with open(self.challengesjson, "r") as file:
            data = json.load(file)
            temp = data["challenges"]
            for i in temp:
                if i["challengeid"] == self.challengeid:
                    i = self.challenge
                    break
        with open(self.challengesjson, "w") as file:
            json.dump(data, file, indent=4)
        with open(self.dragonjson, "r") as file:
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

        with open(self.dragonjson, "w") as file:
            json.dump(data, file, indent=4)
        # pull the winner and loser from the dragon.json file
        with open(self.dragonjson, "r") as file:
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
    c = Combat(997231)
    
    #print(c.challenge)
    #print(c.challenger)
    
    #print(c.challengee)
    
    #winner, loser = c.start_combat()
    c.combat_round()
    #c.log_combat()
    #print(winner)
    
    #print(loser)
