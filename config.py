debug = False

# document the locations of all the files and directories used in the project

# Path to the directory containing the json files
JSON_DIR = "json_files"

#make a string for each json file
DRAGON_JSON = "dragon.json"
CHALLENGES_JSON = "challenges.json"
COMBAT_LOG_JSON = "combat_log.json"
DAMAGE_CHART_JSON = "damage_chart.json"


#create a string for the path to each json file
challengesjson =  JSON_DIR+"/"+CHALLENGES_JSON
dragonjson = JSON_DIR+"/"+DRAGON_JSON
combatlogjson = JSON_DIR+"/"+COMBAT_LOG_JSON
damagechartjson = JSON_DIR+"/"+DAMAGE_CHART_JSON

attributes = ['attack','defense','body','intellect','will','resist','speed','discipline','life','essence']

all_breeds =  ["Red", "Blue", "Silver", "Brown"]
all_ages = {
    1: "Hatchling",
    2: "Childe",
    3: "Young Serpent",
    4: "Serpent",
    5: "Elder Serpent",
    6: "Young Wyrm",
    7: "Wyrm",
    8: "Great Wyrm"
    }

# starting Attributes shared by all breeds

development_points = 0  # devlopment points are used to improve the dragon's stats later in the game or even increase the dragon's age
favor = 0 # favor is used to purchase "Gifts of Gaia" later in the game

#set all remaining stats to 0
attack = 0
defense = 0
body = 0
intellect = 0
will = 0
resist = 0
speed = 0
discipline = 0

# essence 1, age 1, claw attack skill 1, life 5
essence = 1 # essence is used to use skills spells and abilities
age = 1 # age is used to determine the dragon's stats - all dragons start at 1
life = 5 #hit points
wins = 0 # number of wins
losses = 0 # number of losses


claw_attack = 1 # this is a skill
tail_bash = body # this is a skill and always equal to body

starting_breed_stats = {"Red": {"improvement_cost": 8,
                                "aging_cost": 50,
                                "starting_advances": 8,
                                },
                        "Blue": {"improvement_cost": 7,
                                "aging_cost": 55,
                                "starting_advances": 7,
                                },
                        "Silver": {"improvement_cost": 6,
                                "aging_cost": 60,
                                "starting_advances": 6,
                                },
                        "Brown": {"improvement_cost": 5,
                                "aging_cost": 70,
                                "starting_advances": 5,
                                }
                        }
# these are the maximum stats for each breed
breed_stats_ceiling = {"Red" : {"ceiling_attack": 20,"ceiling_defense": 10,"ceiling_body": 15,"ceiling_intellect": 10,"ceiling_will": 10,"ceiling_resist": 10,"ceiling_speed": 10,"ceiling_discipline": 5,"ceiling_life": 35,"ceiling_essence": 15},
                "Blue" : {"ceiling_attack": 15,"ceiling_defense": 15,"ceiling_body": 10,"ceiling_intellect": 15,"ceiling_will": 10,"ceiling_resist": 20,"ceiling_speed": 10,"ceiling_discipline": 10,"ceiling_life": 30,"ceiling_essence": 15},
                "Silver" : {"ceiling_attack": 5,"ceiling_defense": 20,"ceiling_body": 5,"ceiling_intellect": 20,"ceiling_will": 15,"ceiling_resist": 15,"ceiling_speed": 20,"ceiling_discipline": 15,"ceiling_life": 25,"ceiling_essence": 15},
                "Brown" : {"ceiling_attack": 15,"ceiling_defense": 10,"ceiling_body": 20,"ceiling_intellect": 15,"ceiling_will": 15,"ceiling_resist": 10,"ceiling_speed": 5,"ceiling_discipline": 20,"ceiling_life": 30,"ceiling_essence": 20}
                } 
#abilitys attacks and spells per breed  
breed_abilities = {"Red": 
                    {
                        "abilities": {"heal": {"minimum_age": 1}},
                        "skills": {"claw_attack": { "minimum_age": 1},
                                    "tail_bash": { "minimum_age": 1},
                                    "flame_tongue": {"minimum_age": 1},
                                    "double_slash": {"minimum_age": 2},
                                    "molten_horns": {"minimum_age": 3},
                                    "fire_breath": {"minimum_age": 4},
                                    "tail_blaze": {"minimum_age": 4},
                                    "ember_wings": {"minimum_age": 6},
                                    "absoulte_rend": {"minimum_age": 7},
                                    "bezerker_rage": {"minimum_age": 8}},
                        "spells": {}},
                    "Blue":
                        {
                            "abilities": {"heal": {"minimum_age": 1}},
                            "skills": {"claw_attack": { "minimum_age": 1},
                                        "tail_bash": { "minimum_age": 1},
                                        "bitter_chomp": {"minimum_age": 1},
                                        "seaweed_mane": {"minimum_age": 2},
                                        "tail_slash": {"minimum_age": 3},
                                        "poison_breath": {"minimum_age": 3},
                                        "whirlpool_eyes": {"minimum_age": 4}},
                            "spells": {"body_of_water": {"minimum_age": 4},
                                       "oceans_embace": {"minimum_age": 6},
                                       "drain_life": {"minimum_age": 8}}},
                    "Silver":
                        {
                            "abilities": {"heal": {"minimum_age": 1}},
                            "skills": {"claw_attack": { "minimum_age": 1},
                                        "tail_bash": { "minimum_age": 1},
                                        "lightning_breath": {"minimum_age": 2}},
                            "spells": {"refreshing_winds": {"minimum_age": 1},
                                        "wings_of_air": {"minimum_age": 3},
                                        "maddening_winds": {"minimum_age": 4},
                                        "tornado": {"minimum_age": 5},
                                        "vapors_kiss": {"minimum_age": 6},
                                        "gapsp_for_air": {"minimum_age": 7},
                                        "silence": {"minimum_age": 7}}},
                    "Brown":
                        {
                            "abilities": {"heal": {"minimum_age": 1},
                                        "stones_touch": {"minimum_age": 1}},
                            "skills": {"claw_attack": { "minimum_age": 1},
                                        "tail_bash": { "minimum_age": 1},
                                        "mud_slide": {"minimum_age": 2},
                                        "yummy_rock_suprise": {"minimum_age": 3},
                                        "battering_ram": {"minimum_age": 5}},
                            "spells": {"earths_protection": {"minimum_age": 1},
                                        "petrify": {"minimum_age": 6},
                                        "wrath_of_earth": {"minimum_age": 7},
                                        "call_of_gaia": {"minimum_age": 8}}}
}

