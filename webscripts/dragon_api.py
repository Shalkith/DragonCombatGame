import json
import config
from challenges import Challenge
from combat import Combat
from datetime import datetime, timedelta
import random

def get_available_skills(dragon_id):
    dragon = get_dragon(dragon_id)
    age = dragon['age']
    breed = dragon['breed']
    breed_stats = ['attack', 'defense', 'body', 'intellect', 'will', 'resist', 'speed', 'discipline', 'life', 'essence']
    breed_abilities = config.breed_abilities[breed]['abilities']
    breed_skills = config.breed_abilities[breed]['skills']
    breed_spells = config.breed_abilities[breed]['spells']
    available = []
    for stat in breed_stats:
        type = 'stat'
        available.append({'name': stat, 'type': type, 'effect': ''})
    for ability in breed_abilities:
        type = 'abilities'
        if breed_abilities[ability]['minimum_age'] <= age:
            available.append({'name': ability, 'type': type, 'effect': breed_abilities[ability]['effect']})
    for skill in breed_skills:
        type = 'skills'
        if breed_skills[skill]['minimum_age'] <= age:
            available.append({'name': skill, 'type': type, 'effect': breed_skills[skill]['effect']})
    for spell in breed_spells:
        type = 'spells'
        if breed_spells[spell]['minimum_age'] <= age:
            available.append({'name': spell, 'type': type, 'effect': breed_spells[spell]['effect']})
    return available

def can_improve_stat(dragon, stat,available_skills,discipline_level,breed):
    #stat must be in available skills
    for row in available_skills:
        if row['name'] == stat:
            type = row['type']
            break
    else:
        return False, f"{stat} not available to improve",'type'
    #new level cant exceed discipline level
    if type == 'stat':
        currentstat = dragon[stat]
    else:
        try:
            currentstat = dragon[type][stat]
        except KeyError:
            currentstat = 0
    if currentstat+1 > discipline_level and stat != 'discipline' and type != 'stat':
        return False, "Discipline level too low",type
    #if type is stat, it cant exceed the ceiling for the breed
    if type == 'stat':
        ceiling = config.breed_stats_ceiling[breed][f'ceiling_{stat}']
        if currentstat+1 > ceiling:
            return False, f"{stat} has reached the {breed} dragon maximum value of {ceiling}",type
    return True, "Can improve stat",type


def improve_dragon_stat(dragon_id, stat):
    if stat == 'tail_bash':
        return False, "Cannot improve tail_bash directly. It improves automatically with body."
    with open(config.dragonjson, "r") as f:
        dragons = json.load(f)
    for d in dragons["dragons"]:
        if d["id"] == dragon_id:
            advances = d["advances"]
            development_points = d["development_points"]
            breed = d["breed"]
            improvement_cost = config.starting_breed_stats[breed]['improvement_cost']
            if advances <= 0:
                spendtype = "development points"
                available = development_points
            else:
                spendtype = "advances"
                available = advances
            if available <= 0:
                return False, f"Not enough {spendtype} to improve stat"
            if spendtype == "development points":
                if development_points < improvement_cost:
                    return False, f"Not enough development points to improve stat. Need at least {improvement_cost}."
            
            available_skills = get_available_skills(dragon_id)
            can_improve, message,type = can_improve_stat(d, stat, available_skills, d['discipline'], d['breed'])
            if not can_improve:
                return False, message
            if type == 'stat':
                d[stat] += 1
                #if stat is body, also improve tail_bash by 1 automatically
                if stat == 'body':
                    d['skills']['tail_bash'] += 1
            else:
                if stat in d[type]:
                    d[type][stat] += 1
                else:
                    d[type][stat] = 1
            if spendtype == "development points":
                d["development_points"] -= improvement_cost
            else:
                d["advances"] -= 1
            with open(config.dragonjson, "w") as f:
                json.dump(dragons, f, indent=4)
            return True, {"message":f"Improved {stat} of dragon ID {dragon_id}","new_value": d[stat] if type == 'stat' else d[type][stat]}
    return False, "Dragon not found"

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
        # remove dragosn with advances > 0
        dragons["dragons"] = [d for d in dragons["dragons"] if d["advances"] == 0]
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
    status1=check_challenge_status(dragon1["id"])
    status2=check_challenge_status(dragon2["id"])
    if status1:
        return "{} is already in combat.".format(dragon1["name"])
    if status2:
        return "{} is already in combat.".format(dragon2["name"])
    challenge.initiate_challenge(dragon1, dragon2)
    return "{} has challenged {}".format(dragon1["name"], dragon2["name"])



def get_combat_log(challengeid=None):
    # Simulated function to get combat log for a challenge
    jsonfile = 'json_files/combat_log.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        combat_logs = json.load(f)
    if challengeid is None:
        return combat_logs['combat_log']
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

def get_dragons():
    # Simulated function to get all dragons
    jsonfile = 'json_files/dragon.json'
    #read the json file
    with open(jsonfile, 'r') as f:
        dragons_data = json.load(f)
    return dragons_data['dragons']

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