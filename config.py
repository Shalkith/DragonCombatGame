debug = False

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
                                    "flame_tongue": {"name":"Flame Tongue","starting_value":0, "minimum_age": 1},
                                    "double_slash": {"name":"Double Slash","starting_value":0, "minimum_age": 2},
                                    "molten_horns": {"name":"Molten Horns","starting_value":0, "minimum_age": 3},
                                    "fire_breath": {"name":"Fire Breath","starting_value":0, "minimum_age": 4},
                                    "tail_blaze": {"name":"Tail Blaze","starting_value":0, "minimum_age": 4},
                                    "ember_wings": {"name":"Ember Wings","starting_value":0, "minimum_age": 6},
                                    "absoulte_rend": {"name":"Absoulte Rend","starting_value":0, "minimum_age": 7},
                                    "bezerker_rage": {"name":"Bezerker Rage","starting_value":0, "minimum_age": 8}},
                        "spells": {}},
                    "Blue":
                        {
                            "abilities": {"heal": {"name":"Heal" ,"starting_value":0,"minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash","starting_value":0, "minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                        "bitter_chomp": {"name":"Bitter Chomp","starting_value":0, "minimum_age": 1},
                                        "seaweed_mane": {"name":"Seaweed Mane","starting_value":0, "minimum_age": 2},
                                        "tail_slash": {"name":"Tail Slash","starting_value":0, "minimum_age": 3},
                                        "poison_breath": {"name":"Poison Breath","starting_value":0, "minimum_age": 3},
                                        "whirlpool_eyes": {"name":"Whirlpool Eyes","starting_value":0, "minimum_age": 4}},
                            "spells": {"body_of_water": {"name":"Body of Water","starting_value":0, "minimum_age": 4},
                                        "oceans_embace": {"name":"Oceans Embrace","starting_value":0, "minimum_age": 6},
                                        "drain_life": {"name":"Drain Life","starting_value":0, "minimum_age": 8}}},
                    "Silver":
                        {
                            "abilities": {"heal": {"name":"Heal" ,"starting_value":0,"minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash","starting_value":0, "minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                        "lightning_breath": {"name":"Lightning Breath","starting_value":0, "minimum_age": 2}},
                            "spells": {"refreshing_winds": {"name":"Refreshing Winds","starting_value":0, "minimum_age": 1},
                                        "wings_of_air": {"name":"Wings of Air","starting_value":0, "minimum_age": 3},
                                        "maddening_winds": {"name":"Maddening Winds","starting_value":0, "minimum_age": 4},
                                        "tornado": {"name":"Tornado","starting_value":0, "minimum_age": 5},
                                        "vapors_kiss": {"name":"Vapors Kiss","starting_value":0, "minimum_age": 6},
                                        "gapsp_for_air": {"name":"Gasp for Air", "starting_value":0,"minimum_age": 7},
                                        "silence": {"name":"Silence","starting_value":0, "minimum_age": 7}}},
                    "Brown":
                        {
                            "abilities": {"heal": {"name":"Heal","starting_value":0, "minimum_age": 1,"damage_code":None,"damage_rating":None,"duration":"Instant","effect":"increases life","essence_used":2},
                                        "stones_touch": {"name":"Stones Touch" ,"starting_value":0,"minimum_age": 1}},
                        "skills": {"claw_attack": {"name":"Claw Attack","starting_value":1, "minimum_age": 1,"damage_code":"E", "damage_rating":"CurrentSkillLevel","duration":"Instant","effect":"claws opponent","essence_used":1},
                                    "tail_bash": {"name":"Tail Bash", "starting_value":0,"minimum_age": 1,"damage_code":"B", "damage_rating":"CurrentBodyLevel","duration":"Instant","effect":"bashes opponent with tail","essence_used":"CurrentBodyLevel"},
                                        "mud_slide": {"name":"Mud Slide","starting_value":0, "minimum_age": 2},
                                        "yummy_rock_suprise": {"name":"Yummy Rock Suprise","starting_value":0, "minimum_age": 3},
                                        "battering_ram": {"name":"Battering Ram", "starting_value":0,"minimum_age": 5}},
                            "spells": {"earths_protection": {"name":"Earths Protection", "starting_value":0,"minimum_age": 1},
                                        "petrify": {"name":"Petrify","starting_value":0, "minimum_age": 6},
                                        "wrath_of_earth": {"name":"Wrath of Earth", "starting_value":0,"minimum_age": 7},
                                        "call_of_gaia": {"name":"Call of Gaia","starting_value":0, "minimum_age": 8}}}
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