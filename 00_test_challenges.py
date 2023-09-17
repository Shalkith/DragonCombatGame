#create a script that will test the combat.py and challenges.py files by creating a number of challenges 
# and then accepting them and then running the combat and then logging the results
# Import the necessary modules from the same directory a this file
import sys
sys.path.append("shalkith-discordbot/version2")
from combat import Combat
from challenges import Challenge

# Import the necessary modules from the python standard library
import json
import random
import datetime
import config
import dragonlatter
# Create a class that will create a challenge and accept it

def test_challenge(dayssincechallenge,daycheck):
    # test the challenge class - select two random dragons from the dragon.json file and create a challenge between them
    # open the dragon.json file and read the contents
    # only load dragons that do not have a challenge with a status that is not completed
    # only load dragons that have not issued challenges in three days

    with open(config.dragonjson, "r") as f:
        dragons = json.load(f)
    # select a random dragon from the json file
    # select a random dragon that has not issued a challenge in the last three days

    with open(config.challengesjson, "r") as f:
        challenges = json.load(f)
    # get the current date and time
    current_time = datetime.datetime.now()
    # get the date and time three days ago
    three_days_ago = current_time - datetime.timedelta(days=dayssincechallenge)
    
    # create a list of dragons that have not issued a challenge in the last three days
    available_dragons = []
    for d in dragons["dragons"]:
        unavailable = False
        for c in challenges["challenges"]:
            if c["challenger"]["ownerid"] == d["ownerid"] and c["challenger"]["id"] == d["id"] and c["status"] != "completed":
                print('Skipping {} because it has an open challenge'.format(d["name"]))
                unavailable = True
                break
            elif c["challenger"]["ownerid"] == d["ownerid"] and c["challenger"]["id"] == d["id"] and c["status"] == "completed" and c["challenge_completed_time"] < str(three_days_ago) and daycheck:
                print('Skipping {} because it has issued a challenge in the last {} days'.format(d["name"], dayssincechallenge))
                unavailable = True
                break
            else:
                pass
        if unavailable == True:
            continue
        else:
            if config.debug == True:
                print("Adding {} to the list of available dragons".format(d["name"]))
            available_dragons.append(d)
    # if there are no dragons available, raise an error

    if len(available_dragons) == 0:
        raise ValueError("No dragons available")
    
    # select a random dragon from the list of available dragons
    dragon1 = random.choice(available_dragons)
    # select a random dragon within 5 latter positions of the first dragon basted on the latter_position value of the first dragon
    #print(dragon1["latter_position"])
    dragon2 = dragon1 
    # a dragon can not select itself
    # if the dragon is the same as the first dragon, select another dragon 

    while dragon2 == dragon1:
        #select dragon2 but make sure that other dragons are actually available
        if dragon1["latter_position"] - 5 < 0:
            dragon2 = random.choice(dragons['dragons'][0:dragon1["latter_position"] + 5])
        elif dragon1["latter_position"] + 5 > len(dragons['dragons']):
            dragon2 = random.choice(dragons['dragons'][dragon1["latter_position"] - 5:len(dragons['dragons'])])
        else:
            dragon2 = random.choice(dragons['dragons'][dragon1["latter_position"] - 5:dragon1["latter_position"] + 5])
    
    
    # create a challenge between the two dragons
    challenge = Challenge()
    
    challenge.initiate_challenge(dragon1, dragon2)




def challenge_loop(days,daycheck):
        test_challenge(days,daycheck)
        #accept the challenges
        #read the challenges.json file for accepted challenges
        with open(config.challengesjson, "r") as f:
            challenges = json.load(f)
        #for each challenge, accept it
        for i in challenges["challenges"]:
            if i["status"] == "pending":
                challenge = Challenge()
                challenge.accept_challenge(i["challengeid"])
        #run the combat
        #read the challenges.json file for accepted challenges
        with open(config.challengesjson, "r") as f:
            challenges = json.load(f)
        #for each challenge, run the combat
        for i in challenges["challenges"]:
            if i["status"] == "accepted":
                #print(i)
                combat = Combat(i["challengeid"])
                combat.start_combat()

    
if __name__ == "__main__":
    #make a number of challenges
    for i in range(500):
        # there's a 50% chance that a challenge will be created
        days = 3
        daycheck = False
        if random.randint(1,2) == 1:
            #print("Creating a challenge")
            challenge_loop(days,daycheck)
            dragonlatter.create_dragon_html()
        else:
            #print("Not creating a challenge")
            continue
    

    

