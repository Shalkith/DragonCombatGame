debug = False
import random

def clear_screen():
    import os
    # clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

# document the locations of all the files and directories used in the project

# Path to the directory containing the json files
JSON_DIR = "json_files"
template_dir = "html"
#make a string for each json file
DRAGON_JSON_filename = "dragon.json"
CHALLENGES_JSON_filename = "challenges.json"
COMBAT_LOG_JSON_filename = "combat_log.json"
DAMAGE_CHART_JSON_filename = "damage_chart.json"


#create a string for the path to each json file
challengesjson =  JSON_DIR+"/"+CHALLENGES_JSON_filename
dragonjson = JSON_DIR+"/"+DRAGON_JSON_filename
combatlogjson = JSON_DIR+"/"+COMBAT_LOG_JSON_filename
damagechartjson = JSON_DIR+"/"+DAMAGE_CHART_JSON_filename

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

breed_description = {
    "Red": "Red dragons are the most aggressive and combative of all the breeds.",
    "Silver": "Silver dragons are the most intelligent and wise of all the breeds.",
    "Blue": "Blue dragons are the most cunning and stealthy of all the breeds.",
    "Brown": "Brown dragons are the most resilient and enduring of all the breeds."}

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
                        "abilities": {"heal": {"name":"Heal" ,"starting_value":0, "minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash","starting_value":0, "minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                    "flame_tongue": {"name":"Flame Tongue","starting_value":0, "minimum_age": 1,"damage_code":"C", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"Skill and Spells are reduced by attackers flame tongue level. If reduced to zero they may not use that attack","effect_duration":2,"essence_used":4}, 
                                    "double_slash": {"name":"Double Slash","starting_value":0, "minimum_age": 2,"damage_code":"C", "damage_rating":"CurrentSkillLevel Plus CurrentClawAttack","duration":"Instant","effect":None,"essence_used":5},
                                    "molten_horns": {"name":"Molten Horns","starting_value":0, "minimum_age": 3,"damage_code":"C", "damage_rating":"CurrentSkillLevel Plus CurrentAge","duration":"1 combat round","effect":None,"essence_used":8},
                                    "fire_breath": {"name":"Fire Breath","starting_value":0, "minimum_age": 4,"damage_code":"A", "damage_rating":"CurrentSkillLevel","duration":"1 combat round","effect":None,"essence_used":11,"breath_weapon":True},
                                    "tail_blaze": {"name":"Tail Blaze","starting_value":0, "minimum_age": 4,"damage_code":"C", "damage_rating":"CurrentSkillLevel Plus CurrentBody","duration":"Instant","effect":"Victim loses 1 combat die minimum of zero","effect_duration":1,"essence_used":10},            
                                    "absoulte_rend": {"name":"Absoulte Rend","starting_value":0, "minimum_age": 7,"damage_code":"A", "damage_rating":"(CurrentSkillLevel Plus Claw Attack level)*2","duration":"Instant","effect":None,"essence_used":11},
                                    "bezerker_rage": {"name":"Bezerker Rage","starting_value":0, "minimum_age": 8,"damage_code":None, "damage_rating":"CurrentSkill*2","duration":"2 combat turn","effect":"the skill / spell of all attack rises by the damage rating of this skill. may raise passed starting dicipline. current defence rating lowered to zero","essence_used":5}},
                        "spells": {"ember_wings": {"name":"Ember Wings","starting_value":0, "minimum_age": 6,"damage_code":"B", "damage_rating":"CurrentSpellLevel Plus CurrentAge","duration":"Instant","effect":None,"essence_used":6}
                                   }},
                    "Blue":
                        {
                            "abilities": {"heal": {"name":"Heal" ,"starting_value":0,"minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash","starting_value":0, "minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                        "bitter_chomp": {"name":"Bitter Chomp","starting_value":0, "minimum_age": 1,"damage_code":"C", "damage_rating":"CurrentSkillLevel","duration":"0","effect":"0","essence_used":0},
                                        "seaweed_mane": {"name":"Seaweed Mane","starting_value":0, "minimum_age": 2,"damage_code":"C", "damage_rating":"CurrentSkill + Current Age","duration":"0","effect":"0","essence_used":0},
                                        "tail_slash": {"name":"Tail Slash","starting_value":0, "minimum_age": 3,"damage_code":"B", "damage_rating":"CurrentSkillLevel Plus CurrentBody","duration":"0","effect":"0","essence_used":0},
                                        "poison_breath": {"name":"Poison Breath","starting_value":0, "minimum_age": 3,"damage_code":"A", "damage_rating":"CurrentSkillLevel","duration":"0","effect":"0","essence_used":0},
                                        "whirlpool_eyes": {"name":"Whirlpool Eyes","starting_value":0, "minimum_age": 4,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0}},
                            "spells": {"body_of_water": {"name":"Body of Water","starting_value":0, "minimum_age": 4,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "oceans_embace": {"name":"Oceans Embrace","starting_value":0, "minimum_age": 6,"damage_code":"C", "damage_rating":"CurrentSpellLevel","duration":"0","effect":"0","essence_used":0},
                                        "drain_life": {"name":"Drain Life","starting_value":0, "minimum_age": 8,"damage_code":"B", "damage_rating":"CurrentSpellLevel","duration":"0","effect":"0","essence_used":0}}},
                    "Silver":
                        {
                            "abilities": {"heal": {"name":"Heal" ,"starting_value":0,"minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash","starting_value":0, "minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                        "lightning_breath": {"name":"Lightning Breath","starting_value":0, "minimum_age": 2,"damage_code":"C", "damage_rating":"CurrentSkillLevel","duration":"0","effect":"0","essence_used":0}},
                            "spells": {"refreshing_winds": {"name":"Refreshing Winds","starting_value":0, "minimum_age": 1,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "wings_of_air": {"name":"Wings of Air","starting_value":0, "minimum_age": 3,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "maddening_winds": {"name":"Maddening Winds","starting_value":0, "minimum_age": 4,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "tornado": {"name":"Tornado","starting_value":0, "minimum_age": 5,"damage_code":"B", "damage_rating":"CurrentSpellLevel","duration":"0","effect":"0","essence_used":0},
                                        "vapors_kiss": {"name":"Vapors Kiss","starting_value":0, "minimum_age": 6,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "gapsp_for_air": {"name":"Gasp for Air", "starting_value":0,"minimum_age": 7,"damage_code":"Special", "damage_rating":"CurrentSpellLevel","duration":"0","effect":"0","essence_used":0},
                                        "silence": {"name":"Silence","starting_value":0, "minimum_age": 7,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0}}},
                    "Brown":
                        {
                            "abilities": {"heal": {"name":"Heal","starting_value":0, "minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2},
                                        "stones_touch": {"name":"Stones Touch" ,"starting_value":0,"minimum_age": 1,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash", "starting_value":0,"minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                        "mud_slide": {"name":"Mud Slide","starting_value":0, "minimum_age": 2,"damage_code":"D", "damage_rating":"CurrentSkill + CurrentAge","duration":"0","effect":"0","essence_used":0},
                                        "yummy_rock_suprise": {"name":"Yummy Rock Suprise","starting_value":0, "minimum_age": 3,"damage_code":"C", "damage_rating":"CurrentSkillLevel","duration":"0","effect":"0","essence_used":0},
                                        "battering_ram": {"name":"Battering Ram", "starting_value":0,"minimum_age": 5,"damage_code":"B", "damage_rating":"CurrentSkillLevel","duration":"0","effect":"0","essence_used":0}},
                            "spells": {"earths_protection": {"name":"Earths Protection", "starting_value":0,"minimum_age": 1,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "petrify": {"name":"Petrify","starting_value":0, "minimum_age": 6,"damage_code":None, "damage_rating":None,"duration":"0","effect":"0","essence_used":0},
                                        "wrath_of_earth": {"name":"Wrath of Earth", "starting_value":0,"minimum_age": 7,"damage_code":"D", "damage_rating":"CurrentSpell Level // 2 (minimum 1)","duration":"0","effect":"0","essence_used":0},
                                        "call_of_gaia": {"name":"Call of Gaia","starting_value":0, "minimum_age": 8,"damage_code":"Special", "damage_rating":"Special","duration":"0","effect":"0","essence_used":0}}}
                    }


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
    
# Red Dragons (Fire Theme)
red_dragons = [
    "Blazeheart",
    "Emberwing",
    "Infernoflare",
    "Pyroclaw",
    "Ignisfury",
    "Scorchscale",
    "Magmawraith",
    "Flamestrike",
    "Cinderfang",
    "Volcanorider",
    "Heatwavecrest",
    "Charblaze",
    "Infernoflame",
    "Fireclaw",
    "Emberblaze",
    "Blazewing",
    "Pyroheart",
    "Flamedrake",
    "Scorchwing",
    "Magmafire",
]

# Blue Dragons (Water Theme)
blue_dragons = [
    "Aquariusfin",
    "Neptunesurge",
    "Tidaldance",
    "Azurewave",
    "Serenewave",
    "Marinecrest",
    "Cascadescale",
    "Nauticaldepths",
    "Tsunamisurge",
    "Riveratide",
    "Mistralwhisper",
    "Oceanuscrest",
    "Aquanimbus",
    "Neptunefury",
    "Tidalcrystal",
    "Azuremist",
    "Serenesea",
    "Marineflow",
    "Cascadewings",
    "Nauticaltide",
]

# Silver Dragons (Weather Theme)
silver_dragons = [
    "Nimbusstorm",
    "Cyclonewind",
    "Thunderstrike",
    "Tempestsky",
    "Aurorabeam",
    "Zephyrglide",
    "Hailstormfury",
    "Drizzlemist",
    "Celestialight",
    "Stormridercrest",
    "Meteorfall",
    "Galeshadow",
    "Nimbuswings",
    "Cyclonewraith",
    "Thunderstrikebolt",
    "Tempestcloud",
    "Auroradream",
    "Zephyrtalon",
    "Hailstormfrost",
    "Drizzlerain",
]

# Brown Dragons (Earth Theme)
brown_dragons = [
    "Terrascale",
    "Boulderhide",
    "Grootroot",
    "Gaiastrength",
    "Rockyshield",
    "Quakecrusher",
    "Pebbleclaw",
    "Dustywhisker",
    "Granitebeard",
    "Crumblestone",
    "Rootfang",
    "Cliffhanger",
    "Terraearth",
    "Boulderkin",
    "Grootguardian",
    "Gaiamight",
    "Rockyridge",
    "Quakemaw",
    "Pebblepaw",
    "Dustyfur",
]


red_dragons_fname = [
    "Blaze",
    "Ember",
    "Inferno",
    "Pyro",
    "Ignis",
    "Scorch",
    "Magma",
    "Flame",
    "Cinder",
    "Volcano",
    "Heatwave",
    "Char",
    "Fire",
    "Fury",
    "Flare",
    "Dragonfire",
    "Lava",
    "Flamewind",
    "Scald",
    "Blazewing",
]

# Blue Dragons (Water Theme)
blue_dragons_fname = [
    "Aqua",
    "Neptune",
    "Tide",
    "Azure",
    "Serenity",
    "Marine",
    "Cascade",
    "Nautical",
    "Tsunami",
    "River",
    "Mistral",
    "Ocean",
    "Wave",
    "Whisper",
    "Deepsea",
    "Aquatic",
    "Navy",
    "Sapphire",
    "Tidal",
]

# Silver Dragons (Weather Theme)
silver_dragons_fname = [
    "Nimbus",
    "Cyclone",
    "Thunder",
    "Tempest",
    "Aurora",
    "Zephyr",
    "Hailstorm",
    "Drizzle",
    "Celestial",
    "Storm",
    "Meteor",
    "Gale",
    "Bolt",
    "Sky",
    "Lightning",
    "Wind",
    "Twister",
    "Frost",
    "Cloud",
]

# Brown Dragons (Earth Theme)
brown_dragons_fname = [
    "Terra",
    "Boulder",
    "Groot",
    "Gaia",
    "Rocky",
    "Quake",
    "Pebble",
    "Dusty",
    "Granite",
    "Crumble",
    "Root",
    "Cliff",
    "Stone",
    "Mud",
    "Earth",
    "Mountain",
    "Hill",
    "Cave",
    "Valley",
]

#dragon descriptions
yanthas_description = "Where there is sorrow, I will be the tears of anguish. Where there is fear, I will breed nightmares. Where there is betrayal, I will be your hate. Where there is death, I will sustain it. The time Draws near, and I will consume all."

def generate_character_description(tone):

    sub_plans = {
        "ominous": {
            "plans1": [
                "I shall",
                "My flames will",
                "I will",
                "The darkness shall",
                "With vengeance, I shall",
                "I swear to",
                "I'm destined to",
                "My purpose is to",
                "With dread, I shall",
                "In the name of darkness, I will"
            ],
            "plans2": [
                "unleash chaos upon the world,",
                "scorch the earth,",
                "enslave all who oppose me,",
                "rise from the depths of darkness,",
                "consume all in my path,",
                "bring forth the end of days,",
                "awaken the horrors of the abyss,",
                "plunge the world into eternal night,",
                "usher in an era of suffering,",
                "make the world a living nightmare,"
            ]
        },
        "friendly": {
            "plans1": [
                "I aim to",
                "My purpose is to",
                "I will",
                "With kindness as my guide, I shall",
                "In the spirit of friendship, I will",
                "My mission is to",
                "I'm dedicated to",
                "I shall be a source of",
                "With a heart full of compassion, I will",
                "I vow to"
            ],
            "plans2": [
                "protect the realms,",
                "shelter those in need,",
                "foster peace and unity,",
                "share the wisdom of the ages,",
                "spread love and joy,",
                "inspire greatness in others,",
                "nurture the bonds of friendship,",
                "bring harmony to all lands,",
                "ignite the flames of hope,",
                "make the world a better place,"
            ]
        },
        "neutral": {
            "plans1": [
                "I seek to",
                "My goal is to",
                "I will",
                "With curiosity as my driving force, I shall",
                "In pursuit of knowledge, I will",
                "I'm committed to",
                "I shall be a catalyst for",
                "I aim to find",
                "With a thirst for wisdom, I will",
                "I vow to"
            ],
            "plans2": [
                "understand the mysteries of existence,",
                "light the path forward,",
                "strive for equilibrium in all things,",
                "adapt to the ever-changing world,",
                "explore the depths of the unknown,",
                "embrace the flow of time,",
                "unlock the secrets of the cosmos,",
                "maintain balance in all realms,",
                "seek enlightenment and truth,",
                "unravel the fabric of reality,"
            ]
        }
    }
    sub_ambitions = {
        "ominous": {
            "ambitions1": [
                "to conquer",
                "to dominate",
                "to plunge",
                "to engulf",
                "to subjugate",
                "to annihilate",
                "to obliterate",
                "to shroud",
                "to devour",
                "to reign supreme over"
            ],
            "ambitions2": [
                "all lands and skies.",
                "all in darkness.",
                "the world into despair.",
                "everything in chaos.",
                "all in eternal darkness.",
                "the world in everlasting dread.",
                "the world in unending suffering.",
                "the world in an abyss of torment.",
                "the world in a veil of shadows.",
                "all in a never-ending nightmare."
            ]
        },
        "friendly": {
            "ambitions1": [
                "to create",
                "to nurture",
                "to spread",
                "to inspire",
                "to cultivate",
                "to foster",
                "to ignite",
                "to share",
                "to radiate",
                "to bring"
            ],
            "ambitions2": [
                "a harmonious world.",
                "kindness and love.",
                "joy and unity.",
                "greatness in others.",
                "a haven of happiness.",
                "positivity and goodwill.",
                "laughter and camaraderie.",
                "compassion and empathy.",
                "a world filled with smiles.",
                "light to dispel the darkness."
            ]
        },
        "neutral": {
            "ambitions1": [
                "to unravel",
                "to share",
                "to maintain",
                "to adapt to",
                "to explore",
                "to facilitate",
                "to observe",
                "to harmonize",
                "to discover",
                "to guide"
            ],
            "ambitions2": [
                "the secrets of the universe.",
                "the wisdom of discovery.",
                "balance in all realms.",
                "the ever-changing world.",
                "the frontiers of knowledge.",
                "innovation and progress.",
                "the rhythms of existence.",
                "the beauty of adaptation.",
                "the wonders of growth.",
                "the intricate dance of life."
            ]
        }
    }    
    
    if tone in sub_plans and tone in sub_ambitions:
        plans1 = random.choice(sub_plans[tone]["plans1"])
        plans2 = random.choice(sub_plans[tone]["plans2"])
        ambitions1 = random.choice(sub_ambitions[tone]["ambitions1"])
        ambitions2 = random.choice(sub_ambitions[tone]["ambitions2"])
        description = f"{plans1} {plans2} {ambitions1} {ambitions2}"
    else:
        description = "Invalid tone. Please choose 'ominous', 'friendly', or 'neutral'."

    return description

def random_tone(breed):
    if breed == "Red":
        tone = random.choice(["ominous", "ominous", "ominous", "ominous", "friendly", "neutral"])
    elif breed == "Blue":
        tone = random.choice(["friendly", "friendly", "friendly", "friendly", "ominous", "neutral"])
    elif breed == "Silver":
        tone = random.choice(["neutral", "neutral", "neutral", "ominous","friendly", "friendly"])
    elif breed == "Brown":
        tone = random.choice(["neutral", "neutral", "neutral", "ominous", "ominous", "friendly"])
    else:
        tone = "neutral"
    return tone