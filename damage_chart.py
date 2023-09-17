# create a json file called damage_chart.json that contains the following data:
# rows A - E and columns "1-4","5-9", "10-14", "15-19", "20+"
# each of the columns will have two columns one called dice another called bonus
# the dice column will contain the number of dice to roll
# the bonus column will contain the bonus to add to the dice roll

# I will populate each value
import json 
import config

def generate_damagechart():
        damagechartjson = config.damagechartjson

        data = {
                "A": {
                        1:{"dice":2,"bonus":0},2:{"dice":2,"bonus":0},3:{"dice":2,"bonus":0},4:{"dice":2,"bonus":0},
                        5:{"dice":2,"bonus":3},6:{"dice":2,"bonus":3},7:{"dice":2,"bonus":3},8:{"dice":2,"bonus":3},9:{"dice":2,"bonus":3},
                        10:{"dice":3,"bonus":0},11:{"dice":3,"bonus":0},12:{"dice":3,"bonus":0},13:{"dice":3,"bonus":0},14:{"dice":3,"bonus":0},
                        15:{"dice":3,"bonus":3},16:{"dice":3,"bonus":3},17:{"dice":3,"bonus":3},18:{"dice":3,"bonus":3},19:{"dice":3,"bonus":3},
                        20:{"dice":4,"bonus":0}},
                "B": {
                        1:{"dice":1,"bonus":3},2:{"dice":1,"bonus":3},3:{"dice":1,"bonus":3},4:{"dice":1,"bonus":3},
                        5:{"dice":2,"bonus":0},6:{"dice":2,"bonus":0},7:{"dice":2,"bonus":0},8:{"dice":2,"bonus":0},9:{"dice":2,"bonus":0},
                        10:{"dice":2,"bonus":3},11:{"dice":2,"bonus":3},12:{"dice":2,"bonus":3},13:{"dice":2,"bonus":3},14:{"dice":2,"bonus":3},
                        15:{"dice":3,"bonus":0},16:{"dice":3,"bonus":0},17:{"dice":3,"bonus":0},18:{"dice":3,"bonus":0},19:{"dice":3,"bonus":0},
                        20:{"dice":3,"bonus":3}},
                "C": {
                        1:{"dice":1,"bonus":0},2:{"dice":1,"bonus":0},3:{"dice":1,"bonus":0},4:{"dice":1,"bonus":0},
                        5:{"dice":1,"bonus":3},6:{"dice":1,"bonus":3},7:{"dice":1,"bonus":3},8:{"dice":1,"bonus":3},9:{"dice":1,"bonus":3},
                        10:{"dice":2,"bonus":0},11:{"dice":2,"bonus":0},12:{"dice":2,"bonus":0},13:{"dice":2,"bonus":0},14:{"dice":2,"bonus":0},
                        15:{"dice":2,"bonus":3},16:{"dice":2,"bonus":3},17:{"dice":2,"bonus":3},18:{"dice":2,"bonus":3},19:{"dice":2,"bonus":3},
                        20:{"dice":3,"bonus":0}},
                "D": {
                        1:{"dice":1,"bonus":0},2:{"dice":1,"bonus":0},3:{"dice":1,"bonus":0},4:{"dice":1,"bonus":0},
                        5:{"dice":1,"bonus":0},6:{"dice":1,"bonus":0},7:{"dice":1,"bonus":0},8:{"dice":1,"bonus":0},9:{"dice":1,"bonus":0},
                        10:{"dice":1,"bonus":3},11:{"dice":1,"bonus":3},12:{"dice":1,"bonus":3},13:{"dice":1,"bonus":3},14:{"dice":1,"bonus":3},
                        15:{"dice":2,"bonus":0},16:{"dice":2,"bonus":0},17:{"dice":2,"bonus":0},18:{"dice":2,"bonus":0},19:{"dice":2,"bonus":0},
                        20:{"dice":2,"bonus":3}},
                "E": {
                        1:{"dice":1,"bonus":0},2:{"dice":1,"bonus":0},3:{"dice":1,"bonus":0},4:{"dice":1,"bonus":0},
                        5:{"dice":1,"bonus":0},6:{"dice":1,"bonus":0},7:{"dice":1,"bonus":0},8:{"dice":1,"bonus":0},9:{"dice":1,"bonus":0},
                        10:{"dice":1,"bonus":0},11:{"dice":1,"bonus":0},12:{"dice":1,"bonus":0},13:{"dice":1,"bonus":0},14:{"dice":1,"bonus":0},
                        15:{"dice":1,"bonus":3},16:{"dice":1,"bonus":3},17:{"dice":1,"bonus":3},18:{"dice":1,"bonus":3},19:{"dice":1,"bonus":3},
                        20:{"dice":2,"bonus":0}}
                }
        with open(damagechartjson, "w") as file:
                json.dump(data, file, indent=4)


if __name__ == "__main__":
        generate_damagechart()

