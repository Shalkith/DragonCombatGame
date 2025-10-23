from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi import Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import os
import sys
import json 
from hatching_dragons import generatedragons, random_breed
from challenges import Challenge
from itsdangerous import URLSafeSerializer

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'webscripts'))
from webscripts.dragon_api import get_dragon, get_dragons , get_player_dragons, check_challenge_status, cpu_start_challenge, check_for_repeated_name
from webscripts.dragon_api import see_my_challenges, get_combat_log, accept_pending_challenges_loop, run_accepted_challenges_loop,improve_dragon_stat
from webscripts.dragon_html import * 

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
SECRET_KEY = "supersecretkey"
serializer = URLSafeSerializer(SECRET_KEY)

####################
# Helper Functions #
####################

def check_combat_log(challengeid: int) -> dict:
    """Check the combat log for a given challenge ID."""
    log = get_combat_log(challengeid)
    if log:
        return log
    else:
        return {"message": "No combat log found for this challenge ID."}    

def check_if_dragon_in_combat(dragon_id: int) -> bool:
    """Check if a dragon is currently in combat."""
    # Placeholder implementation
    return check_challenge_status(dragon_id)

def check_player_has_dragon(playerid: str) -> bool:
    """Check if a player has at least one dragon."""
    return get_player_dragons(playerid)

######################
# User API Endpoints #   
######################

@app.get("/makeplayerdragon/{playerid}/{breed}/{name}/")
def make_player_dragon(playerid: str, breed: str, name: str):
    """Create a new dragon for a player."""
    has_dragon,userdragon = check_player_has_dragon(playerid)
    if has_dragon:
        return dragon(userdragon[0])
    else:
        if check_for_repeated_name(name):
            return {"error": "Dragon name already exists. Please choose a different name."}
        try:
            succeeded,dragon_ids = generatedragons(name,breed,playerid,1,autogenerage=False)
            if not succeeded:
                return {"error": dragon_ids} 
            return dragon(dragon_ids[0])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/improve/{dragon_id}/{stat}")
def improve_dragon_stat_endpoint(dragon_id: int, stat: str):
    """Improve a specific stat of a dragon."""
    success,message = improve_dragon_stat(dragon_id, stat)
    if success:
        return JSONResponse(
            status_code=200,
            content={
            "success": True,
            "message": message,
            "dragon_id": dragon_id,
            "stat": stat,
            "new_value": message["new_value"]
        })
    else:
        raise HTTPException(
            status_code=400, 
            detail={
                "success": False,
                "message": message,
                "dragon_id": dragon_id,
                "stat": stat
            })

@app.get("/acceptchallenge/{challengeid}")
def accept_challenge(challengeid: int):
    """Accept a challenge by its ID."""
    challenge = Challenge()
    result = challenge.accept_challenge(challengeid)
    return {"message": result}

@app.get("/combatlog/{challengeid}")
def combat_log(challengeid: int):
    """Retrieve the combat log for a given challenge ID."""
    log = check_combat_log(challengeid)
    return log

@app.get("/getcombatlogs")
def get_combat_logs_endpoint():
    """Endpoint to retrieve all combat logs."""
    logs = get_combat_log()
    return {"combat_logs": logs}

@app.get("/mychallenges/{playerid}")
def my_challenges(playerid: str):
    """Retrieve all challenges for a given player."""
    challenges = see_my_challenges(playerid)
    return {"challenges": challenges}

@app.get("/dragon/{dragon_id}")
def dragon(dragon_id: int):
    """Retrieve dragon information by ID."""
    dragon = get_dragon(dragon_id)
    if "error" in dragon:
        raise HTTPException(status_code=404, detail=dragon["error"])
    return dragon

@app.get("/initiatechallenge/{challenger}/{defender}")
def initiate_challenge(challenger: int, defender: int):
    """Initiate a challenge between two dragons."""
    self_chalenge = challenger == defender
    if self_chalenge:
        return {"message": "A dragon cannot challenge itself."}
    
    challenge = Challenge()
    challenger = get_dragon(challenger)
    defender = get_dragon(defender)

    if challenger['advances'] > 0 :
        return {"message": f"{challenger['name']} has not completed hatching and cannot challenge other dragons."}
    if defender['advances'] > 0 :
        return {"message": f"{defender['name']} has not completed hatching and cannot be challenged."}

    d1_latter_position = challenger['latter_position']
    d2_latter_position = defender['latter_position']
    position_diff = abs(d1_latter_position - d2_latter_position)
    if position_diff > 5:
        return {"message": f"{challenger['name']} can only challenge dragons within 5 ranks. {defender['name']} is {position_diff} ranks away."}
    status1 = check_if_dragon_in_combat(challenger['id'])
    if status1:
        return {"message": f"{challenger['name']} is already in combat."}
    status2 = check_if_dragon_in_combat(defender['id'])
    if status2:
        return {"message": f"{defender['name']} is already in combat."}
    challenge.initiate_challenge(challenger, defender)
    return JSONResponse(
            status_code=200,
            content={
            "success": True,
            "message": f"Challenge initiated between {challenger['name']} and {defender['name']}",
        })

    #return {"message": f"Challenge initiated between {challenger['name']} and {defender['name']}"}    

@app.get("/getalldragons")
def latter():
    """Retrieve the current list of dragons."""
    jsonfile = 'json_files/dragon.json'
    with open(jsonfile, 'r') as f:
        latter_data = f.read()
    html_content = render_ladder(json.loads(latter_data))
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/ladder")
async def show_ladder(request: Request):
    jsonfile = 'json_files/dragon.json'
    data = json.load(open(jsonfile))
    dragons = sorted(data["dragons"], key=lambda d: d["latter_position"])
    return templates.TemplateResponse("ladder.html", {"request": request, "dragons": dragons})

#######################
# Admin API Endpoints #
#######################

@app.get("/npc_start_challenge")
def test_challenge_endpoint(days: int = 3, daycheck: bool = False):
    """Test challenge between two dragons."""
    result = cpu_start_challenge(days, daycheck)
    return {"message": result}


@app.get("/acceptallchallenges")
def accept_all_challenges():
    """Accept all pending challenges."""
    result = accept_pending_challenges_loop()
    return {"message": result}

@app.get("/startacceptedcombats")
def start_accepted_combats():
    """Start all accepted combats."""
    result = run_accepted_challenges_loop()
    return {"message": result}

@app.get("/makenpcdragon/{quantity}")
def make_npc_dragon(quantity: int):
    """Generate a specified number of NPC dragons."""
    dragons = []
    try:
        succeeded,dragon_ids = generatedragons('RandomName','RandomBreed','cpu',quantity)
        if not succeeded:
            return {"error": dragon_ids}
        for dragon_id in dragon_ids:
            dragons.append(dragon(dragon_id))
        return {"dragons": dragons}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#################
# Web Endpoints #
#################

@app.get("/test", response_class=HTMLResponse)
async def test_endpoint(request: Request):
    dragons = get_dragons()
    return templates.TemplateResponse(
        "latter.html", {"request": request, "dragons": dragons}
    )


@app.get("/old", response_class=HTMLResponse)
def read_root():
    """Serve the root HTML page."""
    html_content = """
    <html>
        <head>
            <title>Dragon Combat Game API</title>
        </head>
        <body>
            <h1>Welcome to the Dragon Combat Game API</h1>
            <p>Use the endpoints to interact with the game.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/health", summary="Health Check")
def health_check():
    """Check the health of the API and its dependencies."""
    health_status = {"status": "healthy"}
    
    try:
        dependency_status = True  # Replace with actual check
        if not dependency_status:
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["status"] = "degraded"
    return health_status


# -------------------------------
# Simple Session (Cookie) Handling
# -------------------------------
def get_current_user(request: Request):
    user_cookie = request.cookies.get("player")
    if not user_cookie:
        return None
    try:
        return serializer.loads(user_cookie)
    except Exception:
        return None


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, playerid: str = Form(...)):
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie(key="player", value=serializer.dumps(playerid))
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("player")
    return response


# -------------------------------
# Dashboard / Main Player Screen
# -------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    playerid = get_current_user(request)
    if not playerid:
        return RedirectResponse("/")
    
    has_dragon, userdragon = check_player_has_dragon(playerid)
    if not has_dragon:
        return templates.TemplateResponse("dragon.html", {"request": request, "playerid": playerid, "has_dragon": False})
    
    d = get_dragon(userdragon[0])
    return templates.TemplateResponse("dragon.html", {"request": request, "playerid": playerid, "has_dragon": True, "dragon": d,'player_dragon':d,"mydragon":True})

#generic dragons page
@app.get("/dragons/{dragon_id}", response_class=HTMLResponse)
def dashboard(request: Request, dragon_id: int):
    playerid = get_current_user(request)
    if not playerid:
        return RedirectResponse("/")
    
    has_dragon, userdragon = check_player_has_dragon(playerid)
    if has_dragon:
        player_dragon = get_dragon(userdragon[0])
    else:
        player_dragon = False
    
    d = get_dragon(dragon_id)
    mydragon = userdragon[0] == dragon_id if has_dragon else False
    return templates.TemplateResponse("dragon.html", {"request": request, "playerid": playerid, "has_dragon": True, "dragon": d, "mydragon": mydragon,"player_dragon":player_dragon })


@app.post("/create_dragon")
def create_dragon(playerid: str = Form(...), name: str = Form(...), breed: str = Form(...)):
    result = make_player_dragon(playerid, breed, name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return RedirectResponse("/dashboard", status_code=302)


# -------------------------------
# Improve Dragon
# -------------------------------
@app.post("/improve")
def improve_stat(dragon_id: int = Form(...), stat: str = Form(...)):
    result = improve_dragon_stat(dragon_id, stat)
    if not result[0]:
        raise HTTPException(status_code=400, detail=result[1])
    return RedirectResponse("/dashboard", status_code=302)


# -------------------------------
# View and Manage Challenges
# -------------------------------
@app.get("/challenges", response_class=HTMLResponse)
def challenges(request: Request):
    playerid = get_current_user(request)
    challenges = see_my_challenges(playerid)
    return templates.TemplateResponse("challenges.html", {"request": request, "challenges": challenges})


@app.post("/accept_challenge")
def accept_challenge_form(challengeid: int = Form(...)):
    result = accept_challenge(challengeid)
    return RedirectResponse("/challenges", status_code=302)


@app.get("/combatlog/{challengeid}", response_class=HTMLResponse)
def combat_log_view(request: Request, challengeid: int):
    log = check_combat_log(challengeid)
    return templates.TemplateResponse("combatlog.html", {"request": request, "log": log})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
