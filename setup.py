# This script is used to setup the environment. 
# it will create the json_files directory and populate it with the json files

# Import the necessary modules from the python standard library
import os
import json
import random
import datetime
import damage_chart
import dragonlatter
# Import the necessary modules from the same directory as this file
import config

# Create a function that will create the json_files directory if it doesn't exist
def create_json_dir():
    # check if the json_files directory exists
    if os.path.isdir(config.JSON_DIR):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        os.mkdir(config.JSON_DIR)

# Create a function that will create the dragon.json file if it doesn't exist
def create_dragon_json():
    # check if the dragon.json file exists
    if os.path.isfile(config.dragonjson):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        data = {"dragons": []}
        with open(config.dragonjson, "w") as file:
            json.dump(data, file, indent=4)

# Create a function that will create the challenges.json file if it doesn't exist
def create_challenges_json():
    # check if the challenges.json file exists
    if os.path.isfile(config.challengesjson):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        data = {"challenges": []}
        with open(config.challengesjson, "w") as file:
            json.dump(data, file, indent=4)

# Create a function that will create the combat_log.json file if it doesn't exist
def create_combat_log_json():
    # check if the combat_log.json file exists
    if os.path.isfile(config.combatlogjson):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        data = {"combat_log": []}
        with open(config.combatlogjson, "w") as file:
            json.dump(data, file, indent=4)


# generate the first 45 dragons
def generate_dragons():
        import hatching_dragons as hd


        for i in range(1):
            ownerid = 'cpu'        
            hd.generatedragons('name','breed',ownerid,1)

#setup the environment
if __name__ == "__main__":
    create_json_dir()
    create_dragon_json()
    create_challenges_json()
    create_combat_log_json()
    #generate_dragons()
    damage_chart.generate_damagechart()
