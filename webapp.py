from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import os
import sys
import json 
from hatching_dragons import generatedragons, random_breed
from challenges import Challenge

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'webscripts'))
from webscripts.dragon_api import get_dragon, get_dragons , get_player_dragons, check_challenge_status, cpu_start_challenge, check_for_repeated_name
from webscripts.dragon_api import see_my_challenges, get_combat_log, accept_pending_challenges_loop, run_accepted_challenges_loop,improve_dragon_stat
from webscripts.dragon_html import * 

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/test", response_class=HTMLResponse)
async def test_endpoint(request: Request):
    dragons = get_dragons()
    return templates.TemplateResponse(
        "latter.html", {"request": request, "dragons": dragons}
    )

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

@app.get("/improve/{dragon_id}/{stat}")
def improve_dragon_stat_endpoint(dragon_id: int, stat: str):
    """Improve a specific stat of a dragon."""
    success,message = improve_dragon_stat(dragon_id, stat)
    if success:
        return {"message": f"{message}"}
    else:
        raise HTTPException(status_code=400, detail=f"{message}")


@app.get("/npc_start_challenge")
def test_challenge_endpoint(days: int = 3, daycheck: bool = False):
    """Test challenge between two dragons."""
    result = cpu_start_challenge(days, daycheck)
    return {"message": result}

@app.get("/acceptchallenge/{challengeid}")
def accept_challenge(challengeid: int):
    """Accept a challenge by its ID."""
    challenge = Challenge()
    result = challenge.accept_challenge(challengeid)
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

@app.get("/combatlog/{challengeid}")
def combat_log(challengeid: int):
    """Retrieve the combat log for a given challenge ID."""
    log = check_combat_log(challengeid)
    return log

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

@app.get("/makeplayerdragon/{playerid}/{breed}/{name}/")
def make_player_dragon(playerid: str, breed: str, name: str):
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

@app.get("/initiatechallenge/{dragon1}/{dragon2}")
def initiate_challenge(dragon1: int, dragon2: int):
    """Initiate a challenge between two dragons."""
    self_chalenge = dragon1 == dragon2
    if self_chalenge:
        return {"message": "A dragon cannot challenge itself."}
    
    challenge = Challenge()
    challenger = get_dragon(dragon1)
    defender = get_dragon(dragon2)

    if challenger['advances'] > 0 :
        return {"message": f"{challenger['name']} has not completed hatching and cannot challenge other dragons."}
    if defender['advances'] > 0 :
        return {"message": f"{defender['name']} has not completed hatching and cannot be challenged."}

    d1_latter_position = challenger['latter_position']
    d2_latter_position = defender['latter_position']
    position_diff = abs(d1_latter_position - d2_latter_position)
    if position_diff > 5:
        return {"message": f"{challenger['name']} can only challenge dragons within 5 ranks. {defender['name']} is {position_diff} ranks away."}
    status1 = check_if_dragon_in_combat(dragon1)
    if status1:
        return {"message": f"{challenger['name']} is already in combat."}
    status2 = check_if_dragon_in_combat(dragon2)
    if status2:
        return {"message": f"{defender['name']} is already in combat."}
    challenge.initiate_challenge(challenger, defender)
    return {"message": f"Challenge initiated between {challenger['name']} and {defender['name']}"}    

@app.get("/latter")
def latter():
    """Retrieve the current dragon latter."""
    jsonfile = 'json_files/dragon.json'
    with open(jsonfile, 'r') as f:
        latter_data = f.read()

    html_content = render_ladder(json.loads(latter_data))
    
    
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/", response_class=HTMLResponse)
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

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin_base.html", {"request": request})


@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})


@app.get("/admin/dragons", response_class=HTMLResponse)
async def admin_dragons(request: Request):
    dragons = get_dragons()
    return templates.TemplateResponse("admin_dragons.html", {"request": request, "dragons": dragons})


@app.get("/admin/challenges", response_class=HTMLResponse)
async def admin_challenges(request: Request):
    return templates.TemplateResponse("admin_challenges.html", {"request": request})


@app.get("/admin/settings", response_class=HTMLResponse)
async def admin_settings(request: Request):
    return templates.TemplateResponse("admin_settings.html", {"request": request})

@app.get("/admin/generate_dragons", response_class=HTMLResponse)
async def generate_dragons_page(request: Request):
    # This page just serves the UI; no dragons data needed
    return templates.TemplateResponse("admin_generate_dragons.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
