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
        self.combatloop = True


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
        self.challenger = self.challenge["challenger"]
        self.challengee = self.challenge["challengee"]

        # a Rested dragon get 1 bonus combat die for the next turn
        self.challenger["rested_bonus"] = False
        self.challengee["rested_bonus"] = False

        # roll bonus is added to the final result of a roll
        self.challenger["roll_adjustment"] = 0
        self.challengee["roll_adjustment"] = 0

        # attack die bonus - are added to the number of dice rolled for attack role
        self.challenger["attack_die_bonus"] = 0
        self.challengee["attack_die_bonus"] = 0
        
        # defense die bonus - are added to the number of dice rolled for defense role
        self.challenger["defense_die_bonus"] = 0
        self.challengee["defense_die_bonus"] = 0

        # essence cost - are subtracted from the cost of skill or spell
        self.challenger["essence_adjustment"] = 0
        self.challengee["essence_adjustment"] = 0

        self.challenger_actions = actions.Actions(self.challenger)
        self.challengee_actions = actions.Actions(self.challengee)

        self.challenge["log"] = []

    def assign_random_event(self,event,dragon):
        # roll a 6 sided die to determine the event
        # events are as follows:
        # 1. Attacked by slayers - at the beginning of each round, roll a 6 sided die, if the roll is a 1, the dragon takes 1 damage
        # 2. Wrath of Gaia - dragon gets a -3 to all rolls
        # 3. The call of Shalkith - dragon may not flee or be in alliances with others
        # 4. Breath of Gaia - +1 combat die to all defense rolls
        # 5. Wisdom of the Ancients - +1 combat die to all attack rolls
        # 6. The Sage Towers - all spells cost 2 less essence to use
        # add these events to the dragons status effects

        # determine if we're setting self.challenger or self.challengee based on dragon value
        if dragon == 'challenger':
            dragon = self.challenger
        elif dragon == 'challengee':
            dragon = self.challengee
        else:
            raise ValueError("Invalid dragon value")
        
        # if a selected event already exists, do not add it again
        if event == 1:
            if "Attacked by slayers" in dragon["status_effects"]:
                return
            dragon["status_effects"].append("Attacked by slayers")
            self.challenge['log'].append("Slayers have been spotted in the area. They appear to be tracking "+dragon["name"]+" and are closing in on their location")
        elif event == 2:
            if "Wrath of Gaia" in dragon["status_effects"]:
                return
            dragon["status_effects"].append("Wrath of Gaia")
            self.challenge['log'].append("The wrath of Gaia has been invoked. "+dragon["name"]+" will suffer a -3 to all rolls")
            dragon["roll_adjustment"] -= 3
        elif event == 3:
            if "The call of Shalkith" in dragon["status_effects"]:
                return
            dragon["status_effects"].append("The call of Shalkith")
            self.challenge['log'].append(dragon["name"]+" has entered a frenzy as the call of Shalkith has overtaken them. They may not flee or be in alliances with others")
        elif event == 4:
            if "Breath of Gaia" in dragon["status_effects"]:
                return
            dragon["status_effects"].append("Breath of Gaia")
            self.challenge['log'].append("The Breath of Gaia has shrouded "+dragon["name"]+"  in a protective aura. They will receive +1 combat die to all defense rolls")
            dragon["defense_die_bonus"] += 1
        elif event == 5:
            if "Wisdom of the Ancients" in dragon["status_effects"]:
                return
            dragon["status_effects"].append("Wisdom of the Ancients")
            self.challenge['log'].append("The Wisdom of the Ancients has been bestowed upon "+dragon["name"]+". They will receive +1 combat die to all attack rolls")
            dragon["attack_die_bonus"] += 1
        elif event == 6:
            if "The Sage Towers" in dragon["status_effects"]:
                return
            dragon["status_effects"].append("The Sage Towers")
            self.challenge['log'].append(dragon["name"]+" has entered a magical field created by the Sage Towers. All spells will cost 2 less essence to use")
            dragon["essence_adjustment"] -= 2
        else:
            raise ValueError("Invalid event value")
        
        # set the dragon back to self object
        if dragon == self.challenger:
            self.challenger = dragon
        elif dragon == self.challengee:
            self.challengee = dragon
        else:
            raise ValueError("Invalid dragon value")
        








        

      
        
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
            temp.append({"challengeid": self.challengeid, "time_completed": str(self.challenge["challenge_completed_time"]),"rounds": self.challenge["rounds"],
                         "outcome": self.death_note,"log": self.challenge["log"],
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
        # 6. dragon rolls to see if a hit is scored, damage resolution
        # 7. repeat steps 5-6 for each dragon
        # Restart this from step 1 until one dragon is dead

        # step 1. regain essence - if combat step is 1, regain 1 essence
        # do not exceed max essence
        if self.challenge["combat_step"] == 1:
            self.challenge["rounds"] += 1
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
            #print a summary of round 1
            if config.debug:
                print(self.challenger["name"]+"  essence: " + str(self.challenger["essence"]))
                print(self.challengee["name"]+"  essence: " + str(self.challengee["essence"]))

        # step 2. roll for random events - if combat step is 2, roll for random events
        elif self.challenge["combat_step"] == 2:
            if config.debug:
                print("step 2")

            # each dragon must roll a 6 sided die
            challenger_roll = random.randint(1,6)
            challengee_roll = random.randint(1,6)
            # if the roll is a 1, a random event occurs, roll a 6 sided die to determine the event
            if challenger_roll == 1:
                event = random.randint(1,6)
                self.assign_random_event(event,'challenger')
            if challengee_roll == 1:
                event = random.randint(1,6)
                self.assign_random_event(event,'challengee')

                
                


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
            #print a summary of round 2
            if config.debug:
                print(self.challenger["name"]+"  status effects: " + str(self.challenger["status_effects"]))
                print(self.challengee["name"]+"  status effects: " + str(self.challengee["status_effects"]))


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
                elif self.challenger["speed"] > self.challengee["speed"]:
                    self.challenger["active_turn"] = True
                    self.challengee["active_turn"] = False
                elif self.challengee["speed"] > self.challenger["speed"]:
                    self.challenger["active_turn"] = False
                    self.challengee["active_turn"] = True
                else:
                    pass
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
            #print a summary of round 3
            if config.debug:
                print(self.challenger["name"]+"  active turn: " + str(self.challenger["active_turn"]))
                print(self.challengee["name"]+"  active turn: " + str(self.challengee["active_turn"]))


        # step 4 range (movement) - if combat step is 4, roll for range
        elif self.challenge["combat_step"] == 4:
            if config.debug:
                print("step 4")

            # for each dragon in the challenge, determin how many spaces they can move
            # a dragon can move 1 space plus one space for every 10 points of speed rounded down
            # the dragon who's actice_turn is true will move last
            # update the challenge json file with the new location of the dragons
            # for each dragon in the challenge 


            if self.challengee["active_turn"]:
                moves = self.challenger["speed"] // 10 +1
                if config.debug:
                    print('challenger moves',moves)
                for i in range(moves):
                    self.challenger["location"] = self.challenger_actions.move(self.challenger["location"], self.challengee["location"])
                moves = self.challengee["speed"] // 10+1
                if config.debug:
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
            if config.debug:
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
            #print a summary of round 4
            if config.debug:
                print(self.challenger["name"]+"  location: " + str(self.challenger["location"]))
                print(self.challengee["name"]+"  location: " + str(self.challengee["location"]))



        
        elif self.challenge["combat_step"] == 5:
            if config.debug:
                print("step 5")
            rest = False

            # check and see if dragon is being attacked by slayers




            # the dragon who's active_turn is true announces intent
            # for now dragons will only attack with claw attack 

            #pick a random skill spell or ability from self.challenger["skills"] or self.challenger["spells"] or self.challenger["abilities"]
            #if the dragon has enough essence, use the skill spell or ability
            #if the dragon does not have enough essence, use claw attack
            #if the dragon has enough essence, use the skill spell or ability            
            choices = ['skills','spells','abilities']
            choices = ['skills','spells']
            #choices = ['skill']
            

            if self.challenger["active_turn"]:
                self.attacker = self.challenger
                self.attack_actions = self.challenger_actions
                self.defender = self.challengee
            else:
                self.attacker = self.challengee
                self.attack_actions = self.challengee_actions
                self.defender = self.challenger
           
            #check and see if attacker is being attacked by slayers 
            if "Attacked by slayers" in self.attacker["status_effects"]:
                if random.randint(1,6) == 1:
                    self.attacker["life"] -= 1
                    self.challenge["log"].append("Slayers have attacked "+self.attacker["name"]+" and dealt 1 damage")
                    if self.attacker["life"] <= 0:
                        self.challenge["log"].append("Slayers have killed "+self.attacker["name"])
                        self.winner = self.defender
                        self.loser = self.attacker
                        self.finish_combat()
                        return self.winner, self.loser
            while True:
                movetype = random.choice(choices)
                move = 0

                #if health is less than 40% of max health, and has atleast 2 essence, use heal
                if self.attacker["life"] <= self.attacker["max_life"] * .4 and self.attacker["essence"] >= 2:
                    movetype = 'abilities'
                    move = 'heal'
                    missing_health = self.attacker["max_life"] - self.attacker["life"]
                    essence_cost_to_max = missing_health * 2
                    

                elif movetype == 'skills':
                    # select a random skill from the skills dict
                    # only select a skill if the value is greater than 0
                    try:
                        move = random.choice(list(self.attacker["skills"].keys()))
                        if self.attacker["skills"][move] <= 0:
                            continue
                    except:
                        pass

                elif movetype == 'spells':
                    # select a random spell from the spells dict
                    # only select a spell if the value is greater than 0
                    try:
                        move = random.choice(list(self.attacker["spells"].keys()))
                        if self.attacker["spells"][move] <= 0:
                            continue
                    except:
                        pass

                    
                elif movetype == 'abilities':
                    # select a random ability from the abilities dict
                    move = random.choice(list(self.attacker["abilities"].keys()))
                    #print(selection)
                else:
                    raise ValueError("Invalid choice")
                # check if the dragon has enough essence to use the skill spell or ability
                                #for testing we're using only claw attack
                
                #move = 'tail_bash'
                #movetype = 'skills'
                if move == 0:
                    continue
                usable,cost = self.skill_check(move,movetype)
                if usable == False:
                    if config.debug:
                        print("The move {} is not usable by {}".format(move,self.attacker["name"]))
                        input("Press enter to continue")
                    continue
                else:
                    pass

                

                
                if config.debug:

                    print(move)
                    print(cost)

                if self.attacker["essence"] >= cost:
                    if config.debug:
                        print("has enough essence")
                    # if the dragon has enough essence, use the skill spell or ability
                    break
                else:
                    if config.debug:
                        print("does not have enough essence")
                    # set rest to true so dragon will resover essense 
                    # if the dragon does not have enough essence, there is a 20% chance they will rest to regain essence
                    if random.randint(1,5) == 1:
                        rest = True
                        self.attacker["essence"] += 1
                        self.attacker["rested_bonus"] = True
                        break
                    else:
                        continue


            if rest == False:
                roll_log = ''
                if move == 'heal':
                    # essence_cost_to_max or max essence available in multiples of 2, whatever is lower
                    cost = min(self.attacker["essence"],essence_cost_to_max)
                    #restore 1 health for every 2 essence spent
                    heal = cost // 2
                    self.attacker["life"] += heal
                    #if life is above max life, set life to max life
                    if self.attacker["life"] > self.attacker["max_life"]:
                        self.attacker["life"] = self.attacker["max_life"]

                    cost = heal * 2
                    cost += self.attacker["essence_adjustment"]
                    if cost < 1:
                        cost = 1
                    self.attacker["essence"] -= cost

                    #heal_log = self.attacker["name"]+" spent "+str(cost)+" essence to heal "+str(heal)+" health (essence cost adjusted by "+str(self.attacker["essence_adjustment"])+")"
                    #self.challenge["log"].append(heal_log)
                    
                    result = "successful"

                    

                else:
                    result,max_damage,cost,roll_log = self.attack_actions.use(movetype,move,cost,self.attacker,self.defender)
                    
                    self.challenge["log"].append(roll_log)
                    damage = max_damage
                    if config.debug:

                        print(result,max_damage,cost)

                    # if the result is successful and if the attack was a skill subtract the defenders body from the damage
                    if result == "successful" and movetype == "skills":
                        damage -= self.defender["body"]
                    # if the result is successful and if the attack was a spell subtract the defenders resist from the damage
                    elif result == "successful" and movetype == "spells":
                        damage -= self.defender["resist"]

                    #defender must always take at least one damage on a successful attack

                    if damage <= 0 and result == "successful":
                        damage = 1
                    else:
                        damage = max_damage

                    # subtract the damage from the defenders health
                    self.defender["life"] -= damage
                
                #subtract the cost from the attackers essence
                self.attacker["essence"] -= cost

            # set the combat step to 6
            self.challenge["combat_step"] = 6
        
            if self.challenger["active_turn"]:
                self.challenger = self.attacker
                self.challengee = self.defender
            else:
                self.challengee = self.attacker
                self.challenger = self.defender
            
            #print a summary of the attack
            if config.debug:
                print()
                print("Round: "+str(self.challenge["rounds"]))
            if rest:
                lognote = "Round: "+str(self.challenge["rounds"])+" "+self.attacker["name"]+" rested to regain essence"
                self.challenge["log"].append(lognote)
                if config.debug:
                    print(self.attacker["name"] + " rested to regain essence")
                pass
            elif result == "successful" and move == 'heal':
                lognote = "Round: "+str(self.challenge["rounds"])+" "+self.attacker["name"]+" spent "+str(cost)+" essence to heal "+str(heal)+" health (essence cost adjusted by "+str(self.attacker["essence_adjustment"])+")"
                self.challenge["log"].append(lognote)

            elif result == "successful":
                lognote1= "Round: "+str(self.challenge["rounds"])+" "+self.attacker["name"]+" used " + move + " on " + self.defender["name"] + " for " + str(damage) + " damage. "
                lognote2 = self.defender["name"] + " resisted " + str(max_damage-damage) + " damage"
                lognote = lognote1+lognote2
                self.challenge["log"].append(lognote)

                if config.debug:
                    print(self.attacker["name"] + " used " + move + " on " + self.defender["name"] + " for " + str(damage) + " damage")
                    print(self.defender["name"] + " resisted " + str(max_damage-damage) + " damage")
                    pass
            else:
                lognote = "Round: "+str(self.challenge["rounds"])+" "+self.attacker["name"]+" used " + move + " on " + self.defender["name"] + " and missed"
                self.challenge["log"].append(lognote)

                if config.debug:
                    print(self.attacker["name"] + " used " + move + " on " + self.defender["name"] + " and missed")
                pass
            if config.debug:
                print(self.attacker["name"]+"  life: " + str(self.attacker["life"]))
                print(self.defender["name"]+"  life: " + str(self.defender["life"]))

            

                
            # update the challengae json file to reflect the new combat step and the new life and essence values
            with open(self.challengesjson, "r") as file:
                data = json.load(file)
                temp = data["challenges"]
                for i in temp:
                    if i["challengeid"] == self.challengeid:
                        i["combat_step"] = self.challenge["combat_step"]
                        i["challenger"]["life"] = self.challenger["life"]
                        i["challengee"]["life"] = self.challengee["life"]
                        i["challenger"]["essence"] = self.challenger["essence"]
                        i["challengee"]["essence"] = self.challengee["essence"]
                        break

            with open(self.challengesjson, "w") as file:
                json.dump(data, file, indent=4)
            # if the defender is dead, end combat
            if self.defender["life"] <= 0:
                self.winner = self.attacker
                self.loser = self.defender
                self.finish_combat()
                return self.winner, self.loser
            
                
            
            #print a summary of round 5
            if config.debug:
                print(self.challenger["name"]+"  life: " + str(self.challenger["life"]))
                print(self.challengee["name"]+"  life: " + str(self.challengee["life"]))

            
        # step 6. dragon rolls to see if a hit is scored - if combat step is 6, roll to see if a hit is scored
        elif self.challenge["combat_step"] == 6:
            if config.debug:
                print("step 6")
            if self.combatloop == True:
                self.combatloop = False
                self.challenge["combat_step"] = 5
                #set the active_turn to the other dragon
                if self.challenger["active_turn"]:
                    self.challenger["active_turn"] = False
                    self.challengee["active_turn"] = True
                elif self.challengee["active_turn"]:
                    self.challenger["active_turn"] = True
                    self.challengee["active_turn"] = False

            else:
                self.combatloop = True
                self.challenge["combat_step"] = 1
            # update the challengae json file to reflect the new combat step and active turn

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
            #print a summary of round 6
            if config.debug:
                print(self.challenger["name"]+"  active turn: " + str(self.challenger["active_turn"]))
                print(self.challengee["name"]+"  active turn: " + str(self.challengee["active_turn"]))

    def skill_check(self,move,movetype):
        #method to check if a skill or spell is above 0 and if its essense use is less than or equal to the dragons max essence
        # essense used is found in config.breed_abilities
        cost,code = self.retrieve_essense_cost(movetype,move)
        if code == 'not ready' and movetype != 'abilities':
            return False,0
        if config.debug:
            print("checking the essense cost of {} for {}".format(move,self.attacker["name"]))
        if movetype == "skills":
            if self.attacker["skills"][move] <= 0:
                return False,0
            elif cost > self.attacker["max_essence"]:
                return False,0
            else:
                return True,cost
        elif movetype == "spells":
            if self.attacker["spells"][move] <= 0:
                return False,0
            elif cost > self.attacker["max_essence"]:
                return False,0
            else:
                return True,cost
        elif movetype == "abilities":
            if cost > self.attacker["max_essence"]:
                return False,0
            else:
                return True,cost
        else:
            raise ValueError("Invalid movetype")
        
            
    
            

    def start_combat(self):
        # set the status of the challenge to in progress
        self.challenge["status"] = "in progress"

        lognote = "{} (rank {}) challenged {} (rank {}) to combat".format(self.challenger["name"],self.challenger["latter_position"],self.challengee["name"],self.challengee["latter_position"])
        self.challenge["log"].append(lognote)


        if config.debug:
            #print a short summary of each dragon before combat begins:
            print()
            print()
            print("++++++++++++++++++")
            print(self.challenger["name"] + " is challenging " + self.challengee["name"] + " to combat")
            print(self.challenger["name"])
            print("life: " + str(self.challenger["life"]) + " essence: " + str(self.challenger["essence"]))
            print(self.challengee["name"])
            print("life: " + str(self.challengee["life"]) + " essence: " + str(self.challengee["essence"]))
            print()


        # loop combat_round until challenge status is no longer in progress
        while self.challenge["status"] == "in progress":
            self.combat_round()
  
        return self.winner, self.loser
    
    def finish_combat(self):
        #winner will select either "Feed on Rival Dragon essence" or "Offer Rival Dragon as a tribute to Gaia"
        death_choices = ["Feed on Rival Dragon essence", "Offer Rival Dragon as a tribute to Gaia"]
        #pick one randomly
        death_choice = random.choice(death_choices)
        #if death choice is "Feed on Rival Dragon essence": 
        # the winner will gain 1 favor and 10 development points
        # the loser will loses 2 favor and gains 1 development point
        #if death choice is "Offer Rival Dragon as a tribute to Gaia":
        # the winner will gain 3 favor and 5 development points
        # the loser will loses 2 favor and gains 1 development point


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
                    if death_choice == "Feed on Rival Dragon essence":
                        i["favor"] += 1
                        i["development_points"] += 10
                    elif death_choice == "Offer Rival Dragon as a tribute to Gaia":
                        i["favor"] += 3
                        i["development_points"] += 5
                    if self.winner["latter_position"] > self.loser["latter_position"]:
                        i["latter_position"] = self.loser["latter_position"]
                        lognote = "{} defeated {} and advanced to rank {}".format(self.winner["name"],self.loser["name"],self.loser["latter_position"])
                        self.challenge["log"].append(lognote)
                        print(lognote)
                        
                        # advance all dragons that are in a latter position greater than the winner by 1
                        for j in temp:
                            
                            if j["latter_position"] >= i["latter_position"] and j['latter_position'] < self.winner["latter_position"] and j["id"] != self.winner["id"]:
                                j["latter_position"] += 1
                                lognote = "{} fell to rank {}".format(j["name"],j["latter_position"])
                                self.challenge["log"].append(lognote)
                                print(lognote)

                elif i["ownerid"] == self.loser["ownerid"] and i["id"] == self.loser["id"]:
                    i["losses"] += 1
                    if death_choice == "Feed on Rival Dragon essence":
                        i["favor"] -= 2
                        # if favor is less than 0, set it to 0
                        if i["favor"] < 0:
                            i["favor"] = 0

                        i["development_points"] += 1
                    elif death_choice == "Offer Rival Dragon as a tribute to Gaia":
                        i["favor"] -= 2
                        # if favor is less than 0, set it to 0
                        if i["favor"] < 0:
                            i["favor"] = 0
                        i["development_points"] += 1

                    if self.loser["latter_position"] < self.winner["latter_position"]:
                        #i["latter_position"] = self.winner["latter_position"]
                        pass
        if death_choice == "Feed on Rival Dragon essence":
            self.death_note = "{} fed on {}'s essence".format(self.winner["name"],self.loser["name"])
        elif death_choice == "Offer Rival Dragon as a tribute to Gaia":
            self.death_note = "{} offered {} as a tribute to Gaia".format(self.winner["name"],self.loser["name"])
        else:
            raise ValueError("Invalid death choice")



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
                     
        #print a summary of the combat
        #if config.debug:
        print(self.winner["name"] + " defeated " + self.loser["name"] + " in combat")
        print()
        lognote = "{} defeated {} in combat".format(self.winner["name"],self.loser["name"])
        self.challenge["log"].append(lognote)

        # log the combat

        self.log_combat()
        return self.winner, self.loser
    def retrieve_essense_cost(self, skill_spell_or_ability,name):
        cost = config.breed_abilities[self.attacker["breed"]][skill_spell_or_ability][name]["essence_used"]
        code = config.breed_abilities[self.attacker["breed"]][skill_spell_or_ability][name]["damage_code"]
        if code in ['A','B','C','D','E']:
            code = 'ready'
        else:
            code = 'not ready'
        #if cost is not int return error
        if type(cost) != int:
            if cost == 'CurrentBodyLevel':
                cost = self.attacker["body"]
            else:
                print(cost)
                raise ValueError("Invalid cost")
        #return cost
        #check for essence cost bonus
        if skill_spell_or_ability == 'skills':
            cost += self.attacker["essence_adjustment"]
            
        elif skill_spell_or_ability == 'spells':
            cost += self.attacker["essence_adjustment"]
        else:
            pass
        #cost must not be less than 1
        if cost < 1:
            cost = 1
        
        return cost,code


if __name__ == "__main__":
    # test combat class
    c = Combat(739768)
    
    #print(c.challenge)
    #print(c.challenger)
    
    #print(c.challengee)
    
    #winner, loser = c.start_combat()
    c.combat_round()
    #c.log_combat()
    #print(winner)
    
    #print(loser)
