#create a class for a game where you create a dragon to fight other dragons
# the dragon has a name provided by the user
# a breed  -  the breeds are Red, Blue, Silver and Brown
# Attributes: 
#   Attack
#   Defense
#   Body
#   Intellect
#   Will
#   Resist
#   Speed
#   Discipline
#   Life
#   Essence
# Skills:
#   Claw Attack
#   Tail Bash - this is a skill that is equal to the dragon's body score
# Ability:
#   Heal requires 2 essence and heals 1 life for every 2 essence spent - a dragon may not be healed above its max life score

# each dragon will reside in a hierarchy of dragons called the dragon latter with newly created dragons being at the bottom
# dragon attribute and latter data will be stored in a json file



# import the random module
import random
import json 
import math
import os 
import config
import dragonlatter

# create a class for the dragon
class HatchDragon:
    # create a constructor method
    def __init__(self, name, breed, userid):
        self.dragonjson = config.dragonjson
        self.debug = config.debug
        #create an empty dragon.json file if it doesn't exist
        try:
            with open(self.dragonjson , "r") as file:
                pass
        except:
            data = {"dragons": []}
            with open(self.dragonjson , "w") as file:
                json.dump(data, file, indent=4)

        self.name = name
        self.breed = breed
        self.ownerid = userid
        # set the dragon's latter position to by reading the json file
        self.latter_position = self.read_json() + 1 

        # if owner is cpu and latter position is 1 set name to Yanthas, set breed to Red and set description to config.yanthas_description
        if self.ownerid == 'cpu': 
            if self.latter_position == 1:

                self.name = "Yanthas"
                self.breed = "Red"
                self.description = config.yanthas_description
                self.tone = 'ominous'
            else:
                self.tone = config.random_tone(self.breed)
                self.description = config.generate_character_description(self.tone)


        self.id = self.read_json() + 1
        
        #every dragon starts with these same starting scores
        
        self.age = config.age
        self.wins = config.wins
        self.losses = config.losses

        
        # Attributes
        self.attributes = config.attributes

        self.attack = config.attack
        self.defense = config.defense
        self.body = config.body
        self.intellect = config.intellect
        self.will = config.will
        self.resist = config.resist
        self.speed = config.speed
        self.discipline = config.discipline
        self.life = config.life
        self.essence = config.essence

        # skills
        self.tail_bash = config.tail_bash
        self.claw_attack = config.claw_attack

        # Development points and favor are used to improve the dragon's stats or increase the dragon's age
        # Favor is used to purchase "Gifts of Gaia" later in the game
        self.development_points = config.development_points
        self.favor = config.favor



        #create lists to hold the dragon's abilities spells and skills

        self.abilities = []
        self.spells = []
        self.skills = []

        self.abilities_dict = {}
        self.spells_dict = {}
        self.skills_dict = {}


        # set the starting stats based on breed - these are improvement_cost,Aging_cost,starting_advances,Claw Attack (this is a skill),essence and life
        # create a dictionary to hold the breed's stats
        self.stats_starting = config.starting_breed_stats[self.breed]
        self.stats_ceilings = config.breed_stats_ceiling[self.breed]
        self.improvement_cost = self.stats_starting["improvement_cost"]
        self.aging_cost = self.stats_starting["aging_cost"]
        self.starting_advances = self.stats_starting["starting_advances"]

        self.ceiling_attack = self.stats_ceilings["ceiling_attack"]
        self.ceiling_defense = self.stats_ceilings["ceiling_defense"]
        self.ceiling_body = self.stats_ceilings["ceiling_body"]
        self.ceiling_intellect = self.stats_ceilings["ceiling_intellect"]
        self.ceiling_will = self.stats_ceilings["ceiling_will"]
        self.ceiling_resist = self.stats_ceilings["ceiling_resist"]
        self.ceiling_speed = self.stats_ceilings["ceiling_speed"]
        self.ceiling_discipline = self.stats_ceilings["ceiling_discipline"]
        self.ceiling_life = self.stats_ceilings["ceiling_life"]
        self.ceiling_essence = self.stats_ceilings["ceiling_essence"]
        

    def assign_skills_spells_abilities(self):
        # assign skills spells and abilities based on breed and age
        # use self.age to determine what skills spells and abilities the dragon has access to
        # use self.breed to determine what skills spells and abilities the dragon has access to
        # use self.skills, self.spells, and self.abilities to store the skills spells and abilities the dragon has access to

        # use config.breed_abilities[self.breed] to determine what skills spells and abilities the dragon has access to
        # use config.breed_abilities[self.breed]["skills"] to determine what skills the dragon has access to
        # use config.breed_abilities[self.breed]["spells"] to determine what spells the dragon has access to
        # use config.breed_abilities[self.breed]["abilities"] to determine what abilities the dragon has access to

        # each of these has a minimum age, if the dragon's age is less than the minimum age, the dragon does not have access to the skill
        # if the dragon's age is greater than or equal to the minimum age, the dragon has access to the skill
        # if the dragon has access to the skill, add it to the self.skills list

        for skill in config.breed_abilities[self.breed]["skills"]:
            if self.age >= config.breed_abilities[self.breed]["skills"][skill]["minimum_age"]:
                self.skills.append(skill)   
        for spell in config.breed_abilities[self.breed]["spells"]:
            if self.age >= config.breed_abilities[self.breed]["spells"][spell]["minimum_age"]:
                self.spells.append(spell)
        for ability in config.breed_abilities[self.breed]["abilities"]:
            if self.age >= config.breed_abilities[self.breed]["abilities"][ability]["minimum_age"]:
                self.abilities.append(ability)

        # create an attribute for each of the skills, spells and abilities and set it to 0
        # except tail bash which is equal to body and claw attack which is equal to 1

        


        for skill in self.skills:
            setattr(self, skill, 0)
        for spell in self.spells:
            setattr(self, spell, 0)
        for ability in self.abilities:
            setattr(self, ability, 0)

        # set tail bash to equal body
        self.tail_bash = self.body
        # set claw attack to equal 1
        self.claw_attack = 1


        for skill in config.breed_abilities[self.breed]["skills"]:
            if self.age >= config.breed_abilities[self.breed]["skills"][skill]["minimum_age"]:
                # add the skill to the self.skills dict and set value to starting_value
                self.skills_dict[skill] = config.breed_abilities[self.breed]["skills"][skill]["starting_value"]
        for spell in config.breed_abilities[self.breed]["spells"]:
            if self.age >= config.breed_abilities[self.breed]["spells"][spell]["minimum_age"]:
                # add the spell to the self.spells dict and set value to starting_value
                self.spells_dict[spell] = config.breed_abilities[self.breed]["spells"][spell]["starting_value"]
        for ability in config.breed_abilities[self.breed]["abilities"]:
            if self.age >= config.breed_abilities[self.breed]["abilities"][ability]["minimum_age"]:
                # add the ability to the self.abilities dict and set value to starting_value
                self.abilities_dict[ability] = config.breed_abilities[self.breed]["abilities"][ability]["starting_value"]








        
    def cpu_buff(self):



        # if the owner is cpu and latter position is within the top 20, randomly increase the age. it should get closer to 8 as we move closer to position 1
        if self.ownerid == 'cpu':
            if self.latter_position <= 50:
                self.age = random.randint(1,1)
            if self.latter_position <= 30:
                self.age = random.randint(1,2)
            if self.latter_position <= 20:
                self.age = random.randint(2,3)
            if self.latter_position <= 15:
                self.age = random.randint(3,6)
            if self.latter_position <= 10:
                self.age = random.randint(6,7)
            if self.latter_position <= 5:
                self.age = random.randint(7,8)
            if self.latter_position == 1:
                self.age = random.randint(8,8)

        # if the owner is cpu and the latter posisistion is within the top 20, 
        # increase the number of wins and losses to represent the dragons fighting history
        # the higher the age, the more wins the dragon has   
        # lets assume postistion 1 always has 200 wins and 0 losses        
        if self.ownerid == 'cpu':
            if self.latter_position == 1:
                self.wins = 200
                self.losses = 200-self.wins

            else:
                #roll 4 6 sided dice multiply by age to get wins
                # roll 2 6 sided dice age to get losses
                self.wins = (random.randint(1,6) + random.randint(1,6) + random.randint(1,6) + random.randint(1,6)) * self.age
                self.losses = (random.randint(1,6) + random.randint(1,6))

        # assign starting advances for each win and loss. 
        # for each win give 0.5 advances and 1.5 favor rounded down
        # for every 10 losses give 1 advance rounded down
        # for every one loss lose 2 favor. favor can not go below zero
        #  This is to make the cpu dragons more powerful
        if self.ownerid == 'cpu':
            self.starting_advances += math.floor(int(self.wins * 0.5))
            self.favor += math.floor(int(self.wins * .2))
            self.starting_advances -= math.floor(int(self.losses / 10))
            self.favor -= int(self.losses * 2)
            if self.favor < 0:
                self.favor = 0                


    def allocate_points(self):
        
        if self.debug == True:
            print("This is what the Dragon looks like before allocating points")
            print(self.name + " is a " + self.breed + " dragon.")
            print("starting advances: " + str(self.starting_advances))
            print("latter position: " + str(self.latter_position))
            print("age: " + str(self.age))
            print("initial stats:")
            print("attack: " + str(self.attack))
            print("defense: " + str(self.defense))
            print("body: " + str(self.body))
            print("intellect: " + str(self.intellect))
            print("will: " + str(self.will))
            print("resist: " + str(self.resist))
            print("speed: " + str(self.speed))
            print("discipline: " + str(self.discipline))
            print("life: " + str(self.life))
            print("essence: " + str(self.essence))
            print("claw attack: " + str(self.claw_attack))
            print("tail bash: " + str(self.tail_bash))
            print("skills: " + str(self.skills))
            print("spells: " + str(self.spells))
            print("abilities: " + str(self.abilities))
            print("development points: " + str(self.development_points))
            print("favor: " + str(self.favor))
            print()
            input('.')

        # randomly allocate the advancement points
        # the sum of the advancement points must equal the starting_advances for the breed
        # attributes
        while True:
            #track spent points
            spent_points = 0
            while True:
                #pick a random attribute ability or skill to advance
                #if the attribute is already at the breed's limit, pick again
                #if the attribute is not at the breed's limit, advance it by 1

                # randomly pick an attribute ability or skill to advance
                picklist = ["attack", "defense", "body", "intellect", "will", "resist", "speed", "discipline", "life", "essence"]
                # add skills and spells to the list of attributes but dont include tail bash
                for skill in self.skills:
                    if skill != "tail_bash":
                        picklist.append(skill)

                for spell in self.spells:
                    picklist.append(spell)
                # randomly pick an attribute ability or skill to advance
                attribute = random.choice(picklist)
                #print debug messages if debug is set to true
                
                if self.debug == True:
                    input('.')
                    print()
                    print("Attempting to advance " + attribute)
                    print("current value: " + str(getattr(self, attribute)))
                    pass

                # if the selected item has a ceiling, check and see if it is already at the breed's limit then pick again
                if hasattr(self, "ceiling_" + attribute):
                    if getattr(self, attribute) == getattr(self, "ceiling_" + attribute):
                        if self.debug == True:
                            print(attribute+"  already at breed's limit")
                            pass
                        continue
                # if the attribute is not at the breed's limit, advance it by 1
                #else:
                # confirm we're not exceeding discipline for skills and spells found in the skills and spells lists
                if attribute in self.skills or attribute in self.spells:
                    if getattr(self, attribute) >= getattr(self, "discipline"):
                        if self.debug == True:
                            print(attribute+"  exceeds breed's limit")

                        continue

                # advance the attribute by 1
                setattr(self, attribute, getattr(self, attribute) + 1)
                # if the attrubite is a skill spell or ability, add it to the appropriate dict
                if attribute in self.skills:
                    self.skills_dict[attribute] = getattr(self, attribute)
                if attribute in self.spells:
                    self.spells_dict[attribute] = getattr(self, attribute)
                if attribute in self.abilities:
                    self.abilities_dict[attribute] = getattr(self, attribute)

                if self.debug == True:
                    print(attribute+" advanced by 1")
                    print(attribute+" new value: " + str(getattr(self, attribute)))
                    #input('.')
                    pass

                #if body is advanced, tail bash is also advanced to be the same as body
                if attribute == "body":
                    self.tail_bash = self.body
                spent_points += 1
                # if all points are not spent, start over
                if spent_points != self.starting_advances:
                    if self.debug == True:
                        print("spent points: " + str(spent_points))
                        print("starting advances: " + str(self.starting_advances))
                        pass
                    continue
                
                # check to make sure the sum of the advancement points equals the starting_advances for the breed, if not, start over
                # remember to subtract 1 from life and essence and 1 from claw attack and dont count tailbash
                sum_of_attributes = 0
                for attribute in self.attributes:
                    if self.debug == True:
                        print("Attribute "+attribute)
                    if attribute != "life" and attribute != "essence":
                        sum_of_attributes += getattr(self, attribute)
                    elif attribute == "life":
                        sum_of_attributes += getattr(self, attribute) - 5  # subtract 5 for life
                    elif attribute == "essence":
                        sum_of_attributes += getattr(self, attribute) - 1

                sum_of_skills = 0
                for skill in self.skills:
                    if self.debug == True:
                        print("Skill "+skill)
                    if skill != "tail_bash":
                        if skill != "claw_attack":
                            sum_of_skills += getattr(self, skill)
                        else:
                            sum_of_skills += getattr(self, skill)-1
                sum_of_spells = 0
                for spell in self.spells:
                    if self.debug == True:
                        print("Spell "+spell)
                    sum_of_spells += getattr(self, spell)
                
                sum_of_attributes += sum_of_skills
                sum_of_attributes += sum_of_spells

                if sum_of_attributes != self.starting_advances:
                    print(sum_of_attributes)
                    if self.debug == True:
                        print("sum of attributes does not equal starting advances")
                        print("attack: " + str(self.attack))
                        print("defense: " + str(self.defense))
                        print("body: " + str(self.body))
                        print("intellect: " + str(self.intellect))
                        print("will: " + str(self.will))
                        print("resist: " + str(self.resist))
                        print("speed: " + str(self.speed))
                        print("discipline: " + str(self.discipline))
                        print("life: " + str(self.life-5))
                        print("essence: " + str(self.essence-1))
                        #print skills and spells
                        for skill in self.skills:
                            if skill != "tail_bash":
                                if skill != "claw_attack":
                                    print(skill + ": " + str(getattr(self, skill)))
                                else:
                                    print(skill + ": " + str(getattr(self, skill)-1))
                        for spell in self.spells:
                            print(spell + ": " + str(getattr(self, spell)))
                        print("starting advances: " + str(self.starting_advances))
                        pass


                    continue
                # check to see if any value is above the breed's limit, if so, start over
                if self.attack > self.ceiling_attack or self.defense > self.ceiling_defense or self.body > self.ceiling_body or self.intellect > self.ceiling_intellect or self.will > self.ceiling_will or self.resist > self.ceiling_resist or self.speed > self.ceiling_speed or self.discipline > self.ceiling_discipline or self.life > self.ceiling_life or self.essence > self.ceiling_essence:
                    if self.debug == True:
                        print("one or more attributes exceeds breed's limit")
                        pass
                    continue
                # check to see if any value is below 0, if so, start over
                if self.attack < 0 or self.defense < 0 or self.body < 0 or self.intellect < 0 or self.will < 0 or self.resist < 0 or self.speed < 0 or self.discipline < 0 or self.life < 0 or self.essence < 0:
                    if self.debug == True:
                        print("one or more attributes is below 0")
                        pass
                    continue
                #check and see if tail bash is above body, if so, set tail bash to body
                if self.tail_bash > self.body:
                    self.tail_bash = self.body
                #set tailbash in dict to body
                self.skills_dict["tail_bash"] = self.body

            

                #print stats after allocating points if debug is set to true
                if self.debug == True:
                    print("This is what the Dragon looks like after allocating points")
                    print(self.name + " is a " + self.breed + " dragon.")
                    print("starting advances: " + str(self.starting_advances))
                    print("latter position: " + str(self.latter_position))
                    print("age: " + str(self.age))
                    print("initial stats:")
                    print("attack: " + str(self.attack))
                    print("defense: " + str(self.defense))
                    print("body: " + str(self.body))
                    print("intellect: " + str(self.intellect))
                    print("will: " + str(self.will))
                    print("resist: " + str(self.resist))
                    print("speed: " + str(self.speed))
                    print("discipline: " + str(self.discipline))
                    print("life: " + str(self.life))
                    print("essence: " + str(self.essence))
                    print("claw attack: " + str(self.claw_attack))
                    print("tail bash: " + str(self.tail_bash))
                    print("skills: " + str(self.skills))
                    print("spells: " + str(self.spells))
                    print("abilities: " + str(self.abilities))
                    print("development points: " + str(self.development_points))
                    print("favor: " + str(self.favor))
                    print()
                    #input('.')
                    pass
                # break out of the loop
                break
            # break out of the loop
            break
    def advance_age(self):    
        # increase all attributes by 1 for every 1 years of age after 1 but do not exceed the ceiling for the breed 
        if self.age > 1:
            for i in range(self.age - 1):
                self.attack += 1
                self.defense += 1
                self.body += 1
                self.intellect += 1
                self.will += 1
                self.resist += 1
                self.speed += 1
                self.discipline += 1
                self.life += 1
                self.essence += 1
                self.tail_bash = self.body
                # make sure the attributes do not exceed the breed's ceiling
                if self.attack > self.ceiling_attack:
                    self.attack = self.ceiling_attack
                if self.defense > self.ceiling_defense:
                    self.defense = self.ceiling_defense
                if self.body > self.ceiling_body:
                    self.body = self.ceiling_body
                if self.intellect > self.ceiling_intellect:
                    self.intellect = self.ceiling_intellect
                if self.will > self.ceiling_will:
                    self.will = self.ceiling_will
                if self.resist > self.ceiling_resist:
                    self.resist = self.ceiling_resist
                if self.speed > self.ceiling_speed:
                    self.speed = self.ceiling_speed
                if self.discipline > self.ceiling_discipline:
                    self.discipline = self.ceiling_discipline
                if self.life > self.ceiling_life:
                    self.life = self.ceiling_life
                if self.essence > self.ceiling_essence:
                    self.essence = self.ceiling_essence
                if self.tail_bash > self.body:
                    self.tail_bash = self.body
            #print final stats if debug is set to true
            if self.debug == True:
                print("This is what the Dragon looks like after advancing age")
                print(self.name + " is a " + self.breed + " dragon.")
                print("starting advances: " + str(self.starting_advances))
                print("latter position: " + str(self.latter_position))
                print("age: " + str(self.age))
                print("initial stats:")
                print("attack: " + str(self.attack))
                print("defense: " + str(self.defense))
                print("body: " + str(self.body))
                print("intellect: " + str(self.intellect))
                print("will: " + str(self.will))
                print("resist: " + str(self.resist))
                print("speed: " + str(self.speed))
                print("discipline: " + str(self.discipline))
                print("life: " + str(self.life))
                print("essence: " + str(self.essence))
                print("claw attack: " + str(self.claw_attack))
                print("tail bash: " + str(self.tail_bash))
                print("skills: " + str(self.skills))
                print("spells: " + str(self.spells))
                print("abilities: " + str(self.abilities))
                print("development points: " + str(self.development_points))
                print("favor: " + str(self.favor))
                print()
                input('.')
                pass
    def create_dragon(self):
            # if the owner is cpu, call the cpu_buff function
            # this will increase the dragon's stats and age based on its latter position
            # then call the allocate_points function to allocate the advancement points
            # then call the advance_age function to increase the dragon's stats based on its age

            # if the owner is not cpu, ask the user to enter the dragon's stats
            if self.ownerid == 'cpu':
                self.cpu_buff()
                self.assign_skills_spells_abilities()
                self.allocate_points()
                self.advance_age()
                
            else:
                self.assign_skills_spells_abilities()
                while True:


                    
                    tempstartingadvances = self.starting_advances
                    tempattack = self.attack
                    tempdefense = self.defense
                    tempbody = self.body
                    tempintellect = self.intellect
                    tempwill = self.will
                    tempresist = self.resist
                    tempspeed = self.speed
                    tempdiscipline = self.discipline
                    templife = self.life
                    tempessence = self.essence
                    tempclaw_attack = self.claw_attack
                   

                    while tempstartingadvances > 0:
                        # clear the console
                        os.system('cls' if os.name == 'nt' else 'clear')
                        # ask the user to enter the dragon's stats
                        print("You are creating a " + self.breed + " dragon.")
                        print("You have " + str(tempstartingadvances) + " advancement points to spend.")
                        print()
                        print("what would you like to advance?")
                        print("1. attack. (current value: " + str(tempattack) + " limit is " + str(self.ceiling_attack) + ")")
                        print("2. defense. (current value: " + str(tempdefense) + " limit is " + str(self.ceiling_defense) + ")")
                        print("3. body. (current value: " + str(tempbody) + " limit is " + str(self.ceiling_body) + ")")
                        print("4. intellect. (current value: " + str(tempintellect) + " limit is " + str(self.ceiling_intellect) + ")")
                        print("5. will. (current value: " + str(tempwill) + " limit is " + str(self.ceiling_will) + ")")
                        print("6. resist. (current value: " + str(tempresist) + " limit is " + str(self.ceiling_resist) + ")")
                        print("7. speed. (current value: " + str(tempspeed) + " limit is " + str(self.ceiling_speed) + ")")
                        print("8. discipline. (current value: " + str(tempdiscipline) + " limit is " + str(self.ceiling_discipline) + ")")
                        print("9. life. (current value: " + str(templife) + " limit is " + str(self.ceiling_life) + ")")
                        print("10. essence. (current value: " + str(tempessence) + " limit is " + str(self.ceiling_essence) + ")")
                        print("11. claw attack. (current value: " + str(tempclaw_attack) + " limit is " + str(self.ceiling_discipline) + ")")
                    

                        response = input("enter a number: ")
                        if response == "1":
                            tempattack += 1
                            tempstartingadvances -= 1
                        elif response == "2":
                            tempdefense += 1
                            tempstartingadvances -= 1
                        elif response == "3":
                            tempbody += 1
                            tempstartingadvances -= 1
                        elif response == "4":
                            tempintellect += 1
                            tempstartingadvances -= 1
                        elif response == "5":
                            tempwill += 1
                            tempstartingadvances -= 1
                        elif response == "6":
                            tempresist += 1
                            tempstartingadvances -= 1
                        elif response == "7":
                            tempspeed += 1
                            tempstartingadvances -= 1
                        elif response == "8":
                            tempdiscipline += 1
                            tempstartingadvances -= 1
                        elif response == "9":
                            templife += 1
                            tempstartingadvances -= 1
                        elif response == "10":
                            tempessence += 1
                            tempstartingadvances -= 1
                        elif response == "11":
                            # claw attack must be lower than discipline
                            if tempclaw_attack >= tempdiscipline:
                                #print a warning message red text
                                print()
                                print('###############################################')
                                print('###############################################')
                                print()
                                print("claw attack exceeds discipline limit. Please try again.")
                                print()
                                print('###############################################')
                                print('###############################################')
                                print()
                                input('press enter to continue')
                                
                                continue
                            else:
                                tempclaw_attack += 1
                                tempstartingadvances -= 1
                        else:
                            print("invalid response")
                            continue

                    
                    temptail_bash = int(tempbody)
                    # check to see if any value is above the breed's limit, if so, start over
                    if tempattack > self.ceiling_attack:
                        print()
                        print('###############################################')
                        print()
                        print(" You attack value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempdefense > self.ceiling_defense:
                        print()
                        print('###############################################')
                        print()
                        print(" You defense value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempbody > self.ceiling_body:
                        print()
                        print('###############################################')
                        print()
                        print(" You body value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempintellect > self.ceiling_intellect:
                        print()
                        print('###############################################')
                        print()
                        print(" You intellect value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempwill > self.ceiling_will:
                        print()
                        print('###############################################')
                        print()
                        print(" You will value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempresist > self.ceiling_resist:
                        print()
                        print('###############################################')
                        print()
                        print(" You resist value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempspeed > self.ceiling_speed:
                        print()
                        print('###############################################')
                        print()
                        print(" You speed value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempdiscipline > self.ceiling_discipline:
                        print()
                        print('###############################################')
                        print()
                        print(" You discipline value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if templife > self.ceiling_life:
                        print()
                        print('###############################################')
                        print()
                        print(" You life value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    if tempessence > self.ceiling_essence:
                        print()
                        print('###############################################')
                        print()
                        print(" You essence value exceeds the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue


                    

                    # confirm we're not exceeding discipline for skills and spells found in the skills and spells lists above - use the temp variables
                    # exclude tail bash and claw attack if claw attack level 1
                    exceeds_discipline = False
                    for attribute in self.skills: 
                        if attribute != "tail_bash" and attribute != "claw_attack":
                            try:
                                if getattr(self, "temp"+attribute) >= getattr(self, "discipline"):
                                    print(attribute + " exceeds discipline. Please try again.")
                                    exceeds_discipline = True
                            except:
                                pass
                    if tempclaw_attack > 1:
                        if tempclaw_attack >= tempdiscipline:
                            print("claw attack exceeds discipline. Please try again.")
                            exceeds_discipline = True
                    for attribute in self.spells:
                        try:
                            if getattr(self, "temp"+attribute) >= getattr(self, "discipline"):
                                print( attribute + " exceeds discipline Please try again.")
                                exceeds_discipline = True
                        except:
                            pass
                                
                    if exceeds_discipline == True:
                        continue
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("This is what the Dragon looks like after allocating points")
                    print(self.name + " is a " + self.breed + " dragon.")
                    print("latter position: " + str(self.latter_position))
                    print("age: " + str(self.age))
                    print("initial stats:")
                    print("attack: " + str(tempattack))
                    print("defense: " + str(tempdefense))
                    print("body: " + str(tempbody))
                    print("intellect: " + str(tempintellect))
                    print("will: " + str(tempwill))
                    print("resist: " + str(tempresist))
                    print("speed: " + str(tempspeed))
                    print("discipline: " + str(tempdiscipline))
                    print("life: " + str(templife))
                    print("essence: " + str(tempessence))
                    print("claw attack: " + str(tempclaw_attack))
                    print("tail bash: " + str(temptail_bash))
                    print("skills: " + str(self.skills))
                    print("spells: " + str(self.spells))
                    print("abilities: " + str(self.abilities))
                    print("development points: " + str(self.development_points))
                    print("favor: " + str(self.favor))
                    print()
                    response = input("Are you sure you want to create this dragon? (y/n): ")
                    if response == "y":
                        self.attack = tempattack
                        self.defense = tempdefense
                        self.body = tempbody
                        self.intellect = tempintellect
                        self.will = tempwill
                        self.resist = tempresist
                        self.speed = tempspeed
                        self.discipline = tempdiscipline
                        self.life = templife
                        self.essence = tempessence
                        self.claw_attack = tempclaw_attack
                        self.tail_bash = temptail_bash
                        # update the skills ability and spells dicts
                        for skill in self.skills:
                            if skill != "tail_bash":
                                self.skills_dict[skill] = getattr(self, skill)
                        for spell in self.spells:
                            self.spells_dict[spell] = getattr(self, spell)
                        for ability in self.abilities:
                            self.abilities_dict[ability] = getattr(self, ability)
                        # set tailbash in dict to body
                        self.skills_dict["tail_bash"] = self.body
                        
                        break
                    else:
                        continue
    def read_json(self):
        # method to read the json file and know how many dragons exist
        # open the json file
        with open(self.dragonjson , "r") as file:
            # load the json file
            data = json.load(file)
            # return the number of dragons in the json file
            return len(data["dragons"])
    def save_dragon(self):
        # create a method to save the dragon to the json file
        # open the json file
        with open(self.dragonjson , "r") as file:
            # read the file to make sure a dragon with the same name doesnt exist
            data = json.load(file)
            for dragon in data["dragons"]:
                if dragon["name"] == self.name:
                    return
        # open the json file
        with open(self.dragonjson , "r") as file:
            # load the json file
            data = json.load(file)
            #create an empty dictionary to store the dragon's data

            tempdragon = {}
            tempdragon["id"] = self.id
            tempdragon["ownerid"] = self.ownerid
            tempdragon["name"] = self.name
            tempdragon["breed"] = self.breed
            tempdragon["age"] = self.age
            tempdragon["tone"] = self.tone
            tempdragon["description"] = self.description
            tempdragon["attack"] = self.attack
            tempdragon["defense"] = self.defense
            tempdragon["body"] = self.body
            tempdragon["intellect"] = self.intellect
            tempdragon["will"] = self.will
            tempdragon["resist"] = self.resist
            tempdragon["speed"] = self.speed
            tempdragon["discipline"] = self.discipline
            tempdragon["life"] = self.life
            tempdragon["essence"] = self.essence
            tempdragon["skills"] = self.skills_dict
            tempdragon["spells"] = self.spells_dict
            tempdragon["abilities"] = self.abilities_dict
            tempdragon["development_points"] = self.development_points
            tempdragon["favor"] = self.favor
            tempdragon["wins"] = self.wins
            tempdragon["losses"] = self.losses
            tempdragon["latter_position"] = self.latter_position

            # append the dragon to the json file
            data["dragons"].append(tempdragon)

        # open the json file
        with open(self.dragonjson , "w") as file:
            # save the data to the json file
            json.dump(data, file, indent=4)
    def print_stats(self):
        # create a method to print out the dragon's stats
        print("Name: " + self.name)
        print("Breed: " + self.breed)
        print("Attack: " + str(self.attack))
        print("Defense: " + str(self.defense))
        print("Body: " + str(self.body))
        print("Intellect: " + str(self.intellect))
        print("Will: " + str(self.will))
        print("Resist: " + str(self.resist))
        print("Speed: " + str(self.speed))
        print("Discipline: " + str(self.discipline))
        print("Life: " + str(self.life))
        print("Essence: " + str(self.essence))
        print("Age: " + str(self.age))
        print("Latter Position: " + str(self.latter_position))
        print("ID: " + str(self.id))
        print("Owner ID: " + str(self.ownerid))
        print("Claw Attack: " + str(self.claw_attack))
        print("Tail Bash: " + str(self.tail_bash))
        print("Skills: " + str(self.skills))
        print("Spells: " + str(self.spells))
        print("abilities: " + str(self.abilities))

def random_name(breed):
    #generate a function to create a random name - the name should sound like a dragon name
    # use the following seed words to generate a two syllable name

    if breed == "Red":
        seed_words = config.red_dragons
        seed_words_fname = config.red_dragons_fname
    elif breed == "Blue":
        seed_words = config.blue_dragons
        seed_words_fname = config.blue_dragons_fname
    elif breed == "Silver":
        seed_words = config.silver_dragons
        seed_words_fname = config.silver_dragons_fname
    elif breed == "Brown":
        seed_words = config.brown_dragons
        seed_words_fname = config.brown_dragons_fname       
    else:
        seed_words = seed_words
        seed_words_fname = seed_words
        
    # the two syllable name will be made up of two random words from the seed words
    # the same word can not be used twice
    # the first word will be capitalized
    # the second word will be capitalized
    # the two words will be joined together with a space between them
    # the name will be returned
    name = ""
    # generate the first word
    first_word = random.choice(seed_words_fname)
    # generate the second word
    second_word = random.choice(seed_words)
    # make sure the second word is not the same as the first word
    while second_word == first_word or first_word.lower() in second_word.lower() or second_word.lower() in first_word.lower():
        second_word = random.choice(seed_words)
    # capitalize the first word
    first_word = first_word.capitalize()
    # capitalize the second word
    second_word = second_word.capitalize()
    # join the two words together
    name = first_word + " " + second_word

    # return the name
    return name
def random_breed():
        # generate a function to create a random breed
        # the breed will be randomly selected from the following list
        breeds = config.all_breeds
        # return the breed
        return random.choice(breeds),breeds
def generatedragons(name,breed,ownerid,dragoncount):

    dragons = []

    if ownerid == 'cpu':
        #generate n random names
        names = []
        for i in range(dragoncount):
            breed,breeds = random_breed()
            name = random_name(breed)
            
            dragon = HatchDragon(name, breed, ownerid)
            dragon.create_dragon()
            dragons.append(dragon)
            dragon.save_dragon()
            # print the dragon's stats
            dragon.print_stats()    


    else: #ownerid is not cpu
        _,breeds = random_breed()
        if breed not in breeds:
            print("Invalid breed. Options are Red, Blue, Silver, Brown")
            return
        # create a dragon object
        dragon = HatchDragon(name, breed, ownerid)
        dragon.create_dragon()
        # append the dragon object to the list of dragons

        dragons.append(dragon)
        dragon.save_dragon()
        # print the dragon's stats
        dragon.print_stats()
    
    dragonlatter.create_dragon_html()


if __name__ == "__main__":
    config.clear_screen()
    # ask if this dragon is for a user or cpu
    # if the dragon is for a user, ask the user to enter the dragon's namem, breed, and ownerid
    response = input('Is this dragon for a user or cpu? (u/c):')
    if response == 'u':
        
        _,breeds = random_breed()
        while True:
            config.clear_screen()
        # ask user to select a breed from list
            print("Select a breed from the following list:")
            print("1. Red")
            print("2. Blue")
            print("3. Silver")
            print("4. Brown")
            response = input("select your breed: ")
            if response == "1":
                breed = "Red"
            elif response == "2":
                breed = "Blue"
            elif response == "3":
                breed = "Silver"
            elif response == "4":
                breed = "Brown"
            else:
                print("Invalid response. Please try again.")
                input('Press enter to continue')
                continue

            name = input("Enter the dragon's name: ")
            ownerid = input("Enter the dragon's ownerid: ")
            break
        generatedragons(name,breed,ownerid,1)
        
    elif response == 'c':
        #ask how many dragons to generate - only accept a number
        dragoncount = input("How many CPU dragons would you like to generate? ")
        #validate this is a number 
        try:
            dragoncount = int(dragoncount)
        except ValueError:
            print("Invalid number. Please try again.")
        generatedragons('RandomName','RandomBreed','cpu',dragoncount)
    else:
        print("Invalid response. Please try again.")
        
