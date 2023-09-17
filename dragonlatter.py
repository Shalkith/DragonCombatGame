#    read the dragon.json file and create an html file for each dragon
#

def create_dragon_html():
    import json
    import os
    import config
    
    # read the dragon.json file
    with open(config.dragonjson, "r") as file:
        data = json.load(file)
        temp = data["dragons"]
        #sort the dragons by latter position
        temp = sorted(temp, key=lambda k: k['latter_position'])

       
        #create html file with a table showing all dragons
        #columns will be: Dragon Picture based on breed and age, position on latter, Name, Breed, wins,Losses
        # center the table and make the table width 100% 
        # make the table border 1px solid black
        # make the table header background color light blue
        # make the table header text color white
        # make the table header text bold
        # make the table header text centered
        # make the table header text font size 20px
        # make the table header text font family arial
        # make the table header text padding 10px

        # make the table row background color light grey
        # make the table row text color black
        # make the table row text centered
        # make the table row text font size 16px
        # make the table row text font family arial
        # make the table row text padding 10px
        # make table content centered left and right




        # make the table row alternate background color white
        
        with open("html/dragon_latter.html", "w") as file:
            # create an html page for each dragon with their id being the page name 
            #this will exist in the html/dragons folder
             # create a page for each dragon
             # TBD

            file.write("""<html><head><title>Dragon Latter</title></head><body><table style='width: 100%; border: 1px solid black; text-align: center; font-size: 20px; font-family: arial; padding: 10px;'>
            <tr style='background-color: lightblue; color: white; text-align: center; font-size: 20px; font-family: arial; padding: 10px;'>
            <th>Position</th><th>Dragon</th><th>Name</th><th>Breed</th><th>Wins</th><th>Losses</th></tr>""")
            
           
            
            for dragon in temp:
                agename = config.all_ages[dragon["age"]]

                if dragon["latter_position"] == 1:
                    age = 'shalkith'
                elif dragon["age"] == 1:
                    age = 'hatch'
                elif dragon["age"] == 2 or dragon["age"] == 3 or dragon["age"] == 4:
                    age = 'young'
                elif  dragon["age"] == 5 or dragon["age"] == 6 or dragon["age"] == 7:
                    age = 'adult'
                else:
                    age = 'elder'

                image = "../images/{}_{}.png".format(dragon["breed"], age)
                #image size is 100px by 100px

                file.write("""<tr style='background-color: lightgrey; color: black; text-align: center; font-size: 16px; font-family: arial; padding: 10px;'>
                           <td>{}</td><td><img src='{}' width='100px' height='100px'>
                           </td>
                           <td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(dragon["latter_position"], image,dragon["name"], dragon["breed"]+' '+agename, dragon["wins"], dragon["losses"]))

            file.write("</table></body></html>")
            

        
        

if __name__ == "__main__":
    create_dragon_html()

        


# generate 8 photos to show a red dragon in different stages of life from hatchling to great wyrm
