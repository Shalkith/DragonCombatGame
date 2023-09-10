# create a json file called damage_chart.json that contains the following data:
# rows A - E and columns "1-4","5-9", "10-14", "15-19", "20+"
# each of the columns will have two columns one called dice another called bonus
# the dice column will contain the number of dice to roll
# the bonus column will contain the bonus to add to the dice roll

# I will populate each value
import json 
import config

damagechartjson = config.damagechartjson
with open(damagechartjson, "w") as file:
    data = {"A": {"1-4":{"dice": 2, "bonus": 0}, "5-9": {"dice": 2, "bonus": 3}, "10-14": {"dice": 3, "bonus": 0}, "15-19": {"dice": 3, "bonus": 3}, "20+": {"dice": 4, "bonus": 0}},
            "B": {"1-4":{"dice": 1, "bonus": 3}, "5-9": {"dice": 2, "bonus": 0}, "10-14": {"dice": 2, "bonus": 3}, "15-19": {"dice": 3, "bonus": 0}, "20+": {"dice": 3, "bonus": 3}},
            "C": {"1-4":{"dice": 1, "bonus": 0}, "5-9": {"dice": 1, "bonus": 3}, "10-14": {"dice": 2, "bonus": 0}, "15-19": {"dice": 2, "bonus": 3}, "20+": {"dice": 3, "bonus": 0}},
            "D": {"1-4":{"dice": 1, "bonus": 0}, "5-9": {"dice": 1, "bonus": 0}, "10-14": {"dice": 1, "bonus": 3}, "15-19": {"dice": 2, "bonus": 0}, "20+": {"dice": 2, "bonus": 3}},
            "E": {"1-4":{"dice": 1, "bonus": 0}, "5-9": {"dice": 1, "bonus": 0}, "10-14": {"dice": 1, "bonus": 0}, "15-19": {"dice": 1, "bonus": 3}, "20+": {"dice": 2, "bonus": 0}}}

    json.dump(data, file, indent=4)




