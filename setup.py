# This script is used to setup the environment. 
# it will create the json_files directory and populate it with the json files

# Import the necessary modules from the python standard library
import os
import json
import random
import datetime

# Import the necessary modules from the same directory as this file
from config import JSON_DIR, DRAGON_JSON, CHALLENGES_JSON, COMBAT_LOG_JSON, DAMAGE_CHART_JSON

# Create a function that will create the json_files directory if it doesn't exist
def create_json_dir():
    # check if the json_files directory exists
    if os.path.isdir(JSON_DIR):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        os.mkdir(JSON_DIR)

# Create a function that will create the dragon.json file if it doesn't exist
def create_dragon_json():
    # check if the dragon.json file exists
    if os.path.isfile(JSON_DIR+"/"+DRAGON_JSON):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        data = {"dragons": []}
        with open(JSON_DIR+"/"+DRAGON_JSON, "w") as file:
            json.dump(data, file, indent=4)

# Create a function that will create the challenges.json file if it doesn't exist
def create_challenges_json():
    # check if the challenges.json file exists
    if os.path.isfile(JSON_DIR+"/"+CHALLENGES_JSON):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        data = {"challenges": []}
        with open(JSON_DIR+"/"+CHALLENGES_JSON, "w") as file:
            json.dump(data, file, indent=4)

# Create a function that will create the combat_log.json file if it doesn't exist
def create_combat_log_json():
    # check if the combat_log.json file exists
    if os.path.isfile(JSON_DIR+"/"+COMBAT_LOG_JSON):
        # if it does exist, do nothing
        pass
    else:
        # if it doesn't exist, create it
        data = {"combat_log": []}
        with open(JSON_DIR+"/"+COMBAT_LOG_JSON, "w") as file:
            json.dump(data, file, indent=4)


# generate the first 45 dragons
def generate_dragons():
        import hatching_dragons as hd


        for i in range(45):
            #select a random breed
            breed = hd.random_breed()
            #select a random name
            name = hd.random_name()

            ownerid = 'cpu'        
            hd.generatedragons(name,breed,ownerid,1)

#setup the environment
if __name__ == "__main__":
    create_json_dir()
    create_dragon_json()
    create_challenges_json()
    create_combat_log_json()
    #generate_dragons()