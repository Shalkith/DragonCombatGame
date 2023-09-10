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
# create a class for the dragon
class HatchDragon:
    # create a constructor method
    def __init__(self, name, breed, userid):
        self.dragonjson = config.dragonjson



        self.debug = False
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
        # set the dragon's development points to 0
        self.development_points = 0 #devlopment points are used to improve the dragon's stats later in the game or even increase the dragon's age
        # set the dragon's favor to 0
        self.favor = 0 # favor is used to purchase "Gifts of Gaia" later in the game

        #generate a unique id for the dragon that increases by 1 for each dragon created
        self.id = self.read_json() + 1


        #every dragon starts with these same starting scores
        # essence 1, age 1, claw attack skill 1, life 5
        self.essence = 1
        self.age = 1
        self.claw_attack = 1 # this is a skill
        self.life = 5

        #set all remaining stats to 0
        self.attack = 0
        self.defense = 0
        self.body = 0
        self.intellect = 0
        self.will = 0
        self.resist = 0
        self.speed = 0
        self.discipline = 0
        self.tail_bash = 0

        #create lists to hold the dragon's abilitys spells and skills
        self.attributes = ['attack','defense','body','intellect','will','resist','speed','discipline','life','essence']
        self.abilitys = ['heal']
        self.spells = []
        self.skills = ['claw_attack','tail_bash']

        # set the starting stats based on breed - these are improvement_cost,Aging_cost,starting_advances,Claw Attack (this is a skill),essence and life
        if breed == "Red":
            self.improvement_cost = 8
            self.aging_cost = 50
            self.starting_advances = 8
            self.essence = 1
        elif breed == "Blue":
            self.improvement_cost = 7
            self.aging_cost = 55
            self.starting_advances = 7
            self.essence = 1
        elif breed == "Silver":
            self.improvement_cost = 6
            self.aging_cost = 60
            self.starting_advances = 6
            self.essence = 1
        elif breed == "Brown":
            self.improvement_cost = 5
            self.aging_cost = 70
            self.starting_advances = 5
            self.essence = 1


        # red breed attribute
        if breed == "Red":
            self.ceiling_attack = 20
            self.ceiling_defense = 10
            self.ceiling_body = 15
            self.ceiling_intellect = 10
            self.ceiling_will = 10
            self.ceiling_resist = 10
            self.ceiling_speed = 10
            self.ceiling_discipline = 5
            self.ceiling_life = 35
            self.ceiling_essence = 15
        # blue breed attribute
        elif breed == "Blue":
            self.ceiling_attack = 15
            self.ceiling_defense = 15
            self.ceiling_body = 10
            self.ceiling_intellect = 15
            self.ceiling_will = 10
            self.ceiling_resist = 20
            self.ceiling_speed = 10
            self.ceiling_discipline = 10
            self.ceiling_life = 30
            self.ceiling_essence = 15
        # silver breed attribute
        elif breed == "Silver":
            self.ceiling_attack = 5
            self.ceiling_defense = 20
            self.ceiling_body = 5
            self.ceiling_intellect = 20
            self.ceiling_will = 15
            self.ceiling_resist = 15
            self.ceiling_speed = 20
            self.ceiling_discipline = 15
            self.ceiling_life = 25
            self.ceiling_essence = 15
        # brown breed attribute
        elif breed == "Brown":
            self.ceiling_attack = 15
            self.ceiling_defense = 10
            self.ceiling_body = 20
            self.ceiling_intellect = 15
            self.ceiling_will = 15
            self.ceiling_resist = 10
            self.ceiling_speed = 5
            self.ceiling_discipline = 20
            self.ceiling_life = 30
            self.ceiling_essence = 20
        #each dragon starts has a win and loss count of 0
        self.wins = 0
        self.losses = 0
    def cpu_buff(self):
        # if the owner is cpu and the latter posisistion is within the top 20, increase the number of wins and losses to represent the dragons fighting history
        # the lower the position number, the more wins the dragon has   
        # lets assume postistion 1 has 200 wins and 0 losses        
        if self.ownerid == 'cpu':
            if self.latter_position == 1:
                self.wins = 200
                self.losses = 200-self.wins
            if self.latter_position >= 2:
                self.wins = random.randint(150,175)
                self.losses = 200-self.wins
            if self.latter_position >= 3:
                self.wins = random.randint(125,150)
                self.losses = 200-self.wins
            if self.latter_position >= 6:
                self.wins = random.randint(100,125)
                self.losses = 125-self.wins
            if self.latter_position >= 10:
                self.wins = random.randint(75,100)
                self.losses = 100-self.wins
            if self.latter_position >= 15:
                self.wins = random.randint(50,75)
                self.losses = 75-self.wins
            if self.latter_position >= 20:
                self.wins = random.randint(25,50)
                self.losses = 50-self.wins
            if self.latter_position > 20:
                self.wins = 0
                self.losses = random.randint(0,25)

        # assign starting advances for each win and loss. 
        # for each win give 0.5 advances and 1.5 favor rounded down
        # for every 10
        #  losses give 1 advance rounded down
        # for every one loss lose 2 favor. favor can not go below zero
        #  This is to make the cpu dragons more powerful
        if self.ownerid == 'cpu':
            self.starting_advances += math.floor(int(self.wins * 0.5))
            self.favor += math.floor(int(self.wins * .2))
            self.starting_advances -= math.floor(int(self.losses / 10))
            self.favor -= int(self.losses * 2)
            if self.favor < 0:
                self.favor = 0

        # if the owner is cpu and latter position is within the top 20, randomly increase the age. it should get closer to 8 as we move closer to position 1
        if self.ownerid == 'cpu':
            if self.latter_position >= 20:
                self.age = random.randint(1,2)
            if self.latter_position >= 15:
                self.age = random.randint(1,3)
            if self.latter_position <= 10:
                self.age = random.randint(2,6)
            if self.latter_position <= 5:
                self.age = random.randint(3,7)
            if self.latter_position <= 3:
                self.age = random.randint(5,8)
            if self.latter_position == 1:
                self.age = random.randint(8,8)
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
            print("abilitys: " + str(self.abilitys))
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
                if self.attack + self.defense + self.body + self.intellect + self.will + self.resist + self.speed + self.discipline + self.life-5 + self.essence-1 + self.claw_attack-1 != self.starting_advances:
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
                        print("claw attack: " + str(self.claw_attack-1))
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
                    print("abilitys: " + str(self.abilitys))
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
                print("abilitys: " + str(self.abilitys))
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
                self.allocate_points()
                self.advance_age()
            else:
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
                                print("claw attack exceeds breed's limit. Please try again.")
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
                    if tempattack > self.ceiling_attack or tempdefense > self.ceiling_defense or tempbody > self.ceiling_body or tempintellect > self.ceiling_intellect or tempwill > self.ceiling_will or tempresist > self.ceiling_resist or tempspeed > self.ceiling_speed or tempdiscipline > self.ceiling_discipline or templife > self.ceiling_life or tempessence > self.ceiling_essence:
                        print()
                        print('###############################################')
                        print('###############################################')
                        print()
                        print("One or more of your values is above the breed's limit. Please try again.")
                        print()
                        print('###############################################')
                        print('###############################################')
                        print()
                        input('press enter to continue')
                        
                        continue
                    
                    # confirm we're not exceeding discipline for skills and spells found in the skills and spells lists above - use the temp variables
                    # exclude tail bash and claw attack if claw attack level 1
                    exceeds_discipline = False
                    for attribute in self.skills: 
                        if attribute != "tail_bash" and attribute != "claw_attack":
                            if getattr(self, "temp"+attribute) >= getattr(self, "discipline"):
                                print(attribute + " exceeds breed's limit. Please try again.")
                                exceeds_discipline = True
                    if tempclaw_attack > 1:
                        if tempclaw_attack >= tempdiscipline:
                            print("claw attack exceeds breed's limit. Please try again.")
                            exceeds_discipline = True
                    for attribute in self.spells:
                        if getattr(self, "temp"+attribute) >= getattr(self, "discipline"):
                            print( attribute + " exceeds breed's limit. Please try again.")
                            exceeds_discipline = True
                                
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
                    print("abilitys: " + str(self.abilitys))
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
            # append the dragon to the json file
            data["dragons"].append({
                "name": self.name,
                "breed": self.breed,
                "attack": self.attack,
                "defense": self.defense,
                "body": self.body,
                "intellect": self.intellect,
                "will": self.will,
                "resist": self.resist,
                "speed": self.speed,
                "discipline": self.discipline,
                "life": self.life,
                "essence": self.essence,
                "age": self.age,
                "latter_position": self.latter_position,
                "id": self.id,
                "ownerid": self.ownerid,
                "claw_attack": self.claw_attack,
                "tail_bash": self.tail_bash,
                "skills": self.skills,
                "spells": self.spells, 
                "abilitys": self.abilitys,
                "development_points": self.development_points,
                "favor": self.favor,
                "wins": self.wins,
                "losses": self.losses


            })
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
        print("Abilitys: " + str(self.abilitys))

def random_name():
    #generate a function to create a random name - the name should sound like a dragon name
    # use the following seed words to generate a two syllable name
    seed_words = [
    "Fire", "Shadow", "Storm", "Frost", "Dragon", "Serpent", "Thunder", "Magma",
    "Blaze", "Night", "Venom", "Ember", "Ice", "Wyrm", "Aurora", "Lightning",
    "Obsidian", "Ruby", "Sapphire", "Inferno", "Crystal", "Vortex", "Gloom",
    "Talon", "Steel", "Onyx", "Celestial", "Moon", "Sun", "Twilight", "Stormcaller",
    "Earth", "Lava", "Abyss", "Fang", "Ash", "Gale", "Solar", "Lunar", "Frostbite",
    "Crimson", "Void", "Quasar", "Nova", "Doom", "Eclipse", "Blizzard", "Cinder",
    "Volcano", "Mystic", "Molten", "Rune", "Havoc", "Drake", "Wraith", "Tidal",
    "Pulse", "Meteor", "Shadowfang", "Ethereal", "Amber", "Thunderstrike", "Penumbral",
    "Whisper", "Maelstrom", "Ignition", "Ebon", "Plasma", "Sable", "Venomous", "Sorcerer",
    "Ironclad", "Arctic", "Nebula", "Ragnarok", "Basilisk", "Nocturnal", "Cerulean",
    "Phoenix", "Specter", "Xenon", "Titan", "Labyrinth", "Chaos", "Crimsonscale",
    "Flamewing", "Glimmer", "Horizon", "Lorekeeper", "Typhoon", "Scarlet", "Glacial",
    "Nether", "Eclipsewing", "Oblivion", "Frostclaw", "Viper", "Sapphirefire",
    "Cinderheart", "Dragonheart", "Stormblade", "Nightshade", "Moonshadow", "Thunderclaw",
    "Pyroclix", "Sablethorn", "Ebonflame", "Dreadfire"]
    # the two syllable name will be made up of two random words from the seed words
    # the same word can not be used twice
    # the first word will be capitalized
    # the second word will be capitalized
    # the two words will be joined together with a space between them
    # the name will be returned
    name = ""
    # generate the first word
    first_word = random.choice(seed_words)
    # generate the second word
    second_word = random.choice(seed_words)
    # make sure the second word is not the same as the first word
    while second_word == first_word:
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
        breeds = ["Red", "Blue", "Silver", "Brown"]
        # return the breed
        return random.choice(breeds),breeds
def generatedragons(name,breed,ownerid,dragoncount):
    
    
    dragons = []

    if ownerid == 'cpu':
        #generate n random names
        names = []
        for i in range(dragoncount):
            cpudragon = HatchDragon(name, breed, ownerid)
            name = random_name()
            breed,breeds = random_breed()
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


if __name__ == "__main__":
    # ask if this dragon is for a user or cpu
    # if the dragon is for a user, ask the user to enter the dragon's namem, breed, and ownerid
    response = input('Is this dragon for a user or cpu? (u/c):')
    if response == 'u':
        _,breeds = random_breed()
        # ask user to select a breed from list
        breed = input("Enter the dragon's breed: "+breeds)
        if breed not in breeds:
            print("Invalid breed. Options are Red, Blue, Silver, Brown")
        if breed in breeds:
            name = input("Enter the dragon's name: ")
            ownerid = input("Enter the dragon's ownerid: ")
            generatedragons(name,breed,ownerid,1)
        breed = input("Enter the dragon's breed: ")
        ownerid = input("Enter the dragon's ownerid: ")
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
        
