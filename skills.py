# write a json file that will contain attacks (skills and spells) and abilities (heal)

import json
import config 

with open("attacks_abilities.json", "w") as file:
    data = {
            "abilities": {"heal": {"breeds": config.breeds, "minimum_age": 1,"DamageCode": None, "DamageRating": None,"Duration": "Instant","effect": "increases life","EssenceUsed" : 2}},
            "skills": {"claw_attack": { "breeds": config.breeds, "minimum_age": 1,"DamageCode": "E", "DamageRating": "CurrentSkillLevel","Duration": "Instant","effect": "claws opponent","EssenceUsed" : 1},
                       "tail_bash": { "breeds": config.breeds, "minimum_age": 1,"DamageCode": "B", "DamageRating": "CurrentBodyLevel","Duration": "Instant","effect": "bashes opponent with tail","EssenceUsed" : "CurrentBodyLevel"}
            },
            "spells": {"breathweapon": {"minimum_age": 4,"DamageCode": "C", "DamageRating": "CurrentSkillLevel","Duration": "Instant","effect": "breathes fire","EssenceUsed" : 3}}


            } 


# Path: DragonCombatGame/damage_chart.py
