import json
import config
from challenges import Challenge
from combat import Combat
from datetime import datetime, timedelta
import random


def check_for_repeated_name(name):
    with open(config.dragonjson, "r") as f:
        dragons = json.load(f)
    for d in dragons["dragons"]:
        if d["name"].lower() == name.lower():
            return True
    return False

def accept_pending_challenges_loop():
        #accept the challenges
        #read the challenges.json file for accepted challenges
        with open(config.challengesjson, "r") as f:
            challenges = json.load(f)
        #for each challenge, accept it
        #autoaccept pending challenges after 24 hours
        # format 06/08/2024, 14:31:47
        now = datetime.now()

        accepted_challenges = []
        for i in challenges["challenges"]:
            if i["status"] == "pending":
                challenge_time = datetime.strptime(i["challenge_sent_time"], "%m/%d/%Y, %H:%M:%S")
                if now - challenge_time < timedelta(hours=24):
                    continue                
                challenge = Challenge()
                challenge.accept_challenge(i["challengeid"])
                accepted_challenges.append(i["challengeid"])
        return accepted_challenges

def run_accepted_challenges_loop():
        #run the combat
        #read the challenges.json file for accepted challenges
        with open(config.challengesjson, "r") as f:
            challenges = json.load(f)
        #for each challenge, run the combat
        started_combats = []
        for i in challenges["challenges"]:
            if i["status"] == "accepted":
                combat = Combat(i["challengeid"])
                combat.start_combat()
                started_combats.append(i["challengeid"])
        return started_combats



def cpu_start_challenge(dayssincechallenge,daycheck):
    with open(config.dragonjson, "r") as f:
        dragons = json.load(f)
        cpudragons={} 
        cpudragons["dragons"] = [d for d in dragons["dragons"] if d["ownerid"] == "cpu"]
    with open(config.challengesjson, "r") as f:
        challenges = json.load(f)

    current_time = datetime.now()
    three_days_ago = current_time - timedelta(days=dayssincechallenge)
    
    available_dragons = []
    for d in cpudragons["dragons"]:
        unavailable = False
        for c in challenges["challenges"]:
            if c["challenger"]["ownerid"] == d["ownerid"] and c["challenger"]["id"] == d["id"] and c["status"] != "completed":
                unavailable = True
                break
            elif c["challenger"]["ownerid"] == d["ownerid"] and c["challenger"]["id"] == d["id"] and c["status"] == "completed" and c["challenge_completed_time"] < str(three_days_ago) and daycheck:
                unavailable = True
                break
            else:
                pass
        if unavailable == True:
            continue
        else:
            available_dragons.append(d)

    if len(available_dragons) == 0:
        raise ValueError("No dragons available")
    dragon1 = random.choice(available_dragons)
    dragon2 = dragon1 
    while dragon2 == dragon1:
        #select dragon2 but make sure that other dragons are actually available
        if dragon1["latter_position"] - 5 < 0:
            dragon2 = random.choice(dragons['dragons'][0:dragon1["latter_position"] + 5])
        elif dragon1["latter_position"] + 5 > len(dragons['dragons']):
            dragon2 = random.choice(dragons['dragons'][dragon1["latter_position"] - 5:len(dragons['dragons'])])
        else:
            dragon2 = random.choice(dragons['dragons'][dragon1["latter_position"] - 5:dragon1["latter_position"] + 5])
    challenge = Challenge()
    challenge.initiate_challenge(dragon1, dragon2)
    return "{} has challenged {}".format(dragon1["name"], dragon2["name"])



def get_combat_log(challengeid):
    # Simulated function to get combat log for a challenge
    jsonfile = 'json_files/combat_log.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        combat_logs = json.load(f)
    for log in combat_logs['combat_log']:
        if log['challengeid'] == challengeid:
            return log
    return None

def see_my_challenges(playerid):
    # Simulated function to see challenges for a player
    jsonfile = 'json_files/challenges.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        challenges_data = json.load(f)
    player_challenges = []
    for challenge in challenges_data['challenges']:
        if challenge['challenger']['ownerid'] == playerid or challenge['challengee']['ownerid'] == playerid:
            player_challenges.append(challenge)
    return player_challenges

def check_challenge_status(dragon_id):
    # Simulated function to check challenge status of a dragon
    jsonfile = 'json_files/challenges.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        challenges_data = json.load(f)
    for challenge in challenges_data['challenges']:
        if challenge['status'] != 'completed' and dragon_id in [challenge['challenger']['id'], challenge['challengee']['id']]:
            return True
    return False

def get_player_dragons(playerid):
    # Simulated function to get all dragons for a player
    jsonfile = 'json_files/dragon.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        dragons_data = json.load(f)
    player_dragons = []
    has_dragon = False
    for dragon in dragons_data['dragons']:
        try:
            if dragon['ownerid'] == playerid:
                player_dragons.append(dragon['id'])
                has_dragon = True
        except KeyError:
            continue
        
    return has_dragon,player_dragons

def get_dragon(dragon_id):
    # Simulated function to get dragon data
    jsonfile = 'json_files/dragon.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        dragons_data = json.load(f)
    for dragon in dragons_data['dragons']:
        try:
            if dragon['id'] == dragon_id:
                return dragon
        except KeyError:
            continue
        
    return{"error": "Dragon not found"}