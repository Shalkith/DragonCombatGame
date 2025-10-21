import requests 
from config import tone_description

class OllamaHelper:
    def __init__(self, model="llama3.2", temperature=1):
        self.url = "http://192.168.99.113:11434/api/chat"
        self.headers = {"Content-Type": "application/json"}
        self.model = model
        self.temperature = temperature

    
    def generate_name(self,breed,tone):
        messages = [
        {"role": "system", "content": f"""You are a {tone} {breed} dragon.You must choose a unique name that reflects your breed and personality.
                Your name should:
                - sound ancient or draconic (e.g., 'Vorthalax', 'Serathryn', 'Kraethis'),
                - avoid any existing dragon names from books or games,
                - be 1 word, 3–10 letters long,
                - feel original, powerful, and fitting for your tone and lineage.
                Respond with only your name — no punctuation or explanation."""},
        {"role": "user", "content": "What is your name?"}
        ]
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json().get("message", {}).get("content", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
        
    

    def generate_description(self,breed,name,tone):

        tone_desc = tone_description[tone]
        
        messages = [
        {"role": "system", "content": "You are one of the ancient and monstrous dragons of myth, awakened by the screams of a dying Earth. Others like you have already risen to assume their part in the titanic struggle for dominance. The sky trembles with the roars of your enemies. The ground is littered with the corpses of the fallen. Now it is your time to heed the call of Earth. Choose your breed, improve your attributes, train your powers, grovel for the gifts of Gaia, and rise and conquer your kin to become the last – to become the Shalkith."},
        {"role": "system", "content": "Shalkith is the title of the ruler of all dragons, the one who has conquered all others and claimed dominion over the world. As a dragon aspiring to become the Shalkith, you must navigate a world filled with peril and opportunity. You will need to make strategic decisions about how to grow your power, form alliances, and defeat your rivals. Your ultimate goal is to become the last dragon standing, the Shalkith, ruling over all other dragons and shaping the fate of the world."},
        {"role": "system", "content": f"You are a {breed} dragon. Your name is {name} but you dont need to tell the user that. They already know. Answer the user's questions accordingly. Do not use any actiobn text or brackets."},
        {"role": "system", "content": f"{tone_desc}"},
        {"role": "user", "content": """
         Give me a 3 sentence introduction about yourself and your goals. 
         Do not mention your name. Do not say "as a {breed} dragon" or "I am a {breed} dragon".
         Do not use the word {tone} in the description."""}
    ]
        
       
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json().get("message", {}).get("content", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    


if __name__ == "__main__":
    breed = 'Red'
    tone = 'Friendly'
    helper = OllamaHelper()
    name = helper.generate_name(breed, tone)
    print(name)
    description = helper.generate_description(breed, name, tone)
    print(description)