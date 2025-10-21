import html
from typing import Dict, List
from config import all_ages

AGE_MAP = all_ages

def safe(s):
    """Escape text for HTML and convert None to empty string."""
    if s is None:
        return ""
    return html.escape(str(s))

def image_for_dragon(dragon: Dict) -> str:
    """Return image path string for a dragon given breed/age/position rules."""
    breed = dragon.get("breed", "unknown").lower()
    pos = dragon.get("latter_position")
    # if champion (position 1) special shalkith image
    if pos == 1:
        return f"images/{breed}_shalkith.png"
    age_key = dragon.get("age", 0)
    age_name = AGE_MAP.get(age_key, "adult").lower().replace(" ", "_")
    return f"images/{breed}_{age_name}.png"

def stats_html(dragon: Dict) -> str:
    keys = ["attack","defense","body","intellect","will","resist","speed","discipline","life","essence"]
    parts = []
    for k in keys:
        parts.append(f"""
        <div class="stat">
            <div class="stat-name">{html.escape(k.capitalize())}</div>
            <div class="stat-value">{safe(dragon.get(k, 0))}</div>
        </div>""")
    return "\n".join(parts)

def dict_list_html(d: Dict, title: str) -> str:
    if not d:
        return f"<div class='subsection'><h4>{html.escape(title)}</h4><div class='empty'>(none)</div></div>"
    items = []
    for k, v in d.items():
        items.append(f"<div class='kv'><span class='k'>{html.escape(k.replace('_',' ').capitalize())}</span><span class='v'>{safe(v)}</span></div>")
    return f"<div class='subsection'><h4>{html.escape(title)}</h4><div class='kv-list'>\n{''.join(items)}\n</div></div>"

def render_ladder(data: Dict) -> str:
    """
    Accepts { "dragons": [ ... ] } and returns an HTML string representing the ranked ladder.
    """
    dragons: List[Dict] = data.get("dragons", [])
    # sort by ladder position (latter_position ascending)
    dragons_sorted = sorted(dragons, key=lambda d: d.get("latter_position", 9999))
    
    cards_html = []
    for d in dragons_sorted:
        name = safe(d.get("name","Unnamed"))
        breed = safe(d.get("breed","Unknown"))
        tone = safe(d.get("tone",""))
        position = d.get("latter_position", 0)
        img = image_for_dragon(d)
        age_label = AGE_MAP.get(d.get("age",0), "Unknown")
        description_raw = d.get("description", "")
        # preserve line breaks: convert to <p> blocks
        desc_paras = "\n".join(f"<p>{html.escape(p.strip())}</p>" for p in description_raw.splitlines() if p.strip())
        if desc_paras == "":
            desc_paras = "<p><em>No description.</em></p>"

        favor = safe(d.get("favor",0))
        wins = safe(d.get("wins",0))
        losses = safe(d.get("losses",0))
        owner = safe(d.get("ownerid",""))
        
        skills_html = dict_list_html(d.get("skills", {}), "Skills")
        spells_html = dict_list_html(d.get("spells", {}), "Spells")
        abilities_html = dict_list_html(d.get("abilities", {}), "Abilities")
        
        card = f"""
        <div class="card">
            <div class="card-left">
                <div class="rank-badge">#{safe(position)}</div>
                <img class="dragon-img" src="{html.escape(img)}" alt="{name} image" onerror="this.onerror=null;this.src='images/placeholder.png'">
                <div class="basic">
                    <h3 class="name">{name}</h3>
                    <div class="meta">{breed} • {age_label} • Owner: {owner}</div>
                </div>
            </div>

            <div class="card-right">
                <div class="description">
                    {desc_paras}
                </div>

                <div class="stats-grid">
                    {stats_html(d)}
                </div>

                <div class="bottom-row">
                    <div class="favor">
                        <div class="favor-label">Favor: {favor}</div>
                        <div class="favor-bar"><div class="favor-fill" style="width: {min(max(int(d.get('favor',0)),0),100)}%"></div></div>
                    </div>
                    <div class="record">
                        <div>Wins: <strong>{wins}</strong></div>
                        <div>Losses: <strong>{losses}</strong></div>
                    </div>
                </div>

                <div class="subsections">
                    {skills_html}
                    {spells_html}
                    {abilities_html}
                </div>
            </div>
        </div>
        """
        cards_html.append(card)
    
    full_html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Dragon Ladder</title>
<style>
/* ====== Basic layout ====== */
:root {{
    --bg: #0f1724;
    --card: #0b1220;
    --muted: #9aa6b2;
    --accent: #c77d6a;
    --accent-2: #5aa6e6;
    --glass: rgba(255,255,255,0.04);
}}
body {{
    margin:0;
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    background: linear-gradient(180deg,#071022 0%, #0f1724 100%);
    color: #e6eef6;
    padding: 28px;
}}
.container {{
    max-width: 1200px;
    margin: 0 auto;
}}

/* Ladder title */
.header {{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 16px;
    margin-bottom: 18px;
}}
.header h1 {{
    margin:0;
    font-size: 24px;
    letter-spacing: -0.02em;
}}
.header .subtitle {{
    color: var(--muted);
    font-size: 13px;
}}

/* Cards grid */
.cards {{
    display:grid;
    grid-template-columns: 1fr;
    gap: 14px;
}}
@media(min-width:900px) {{
    .cards {{ grid-template-columns: 1fr 1fr; }}
}}
.card {{
    display:flex;
    gap: 16px;
    background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.04);
    padding: 14px;
    border-radius: 12px;
    align-items:flex-start;
    box-shadow: 0 6px 20px rgba(2,6,23,0.6);
}}
.card-left {{
    width: 220px;
    min-width: 180px;
    text-align:center;
    position:relative;
}}
.dragon-img {{
    width:160px;
    height:160px;
    object-fit:contain;
    background: var(--glass);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.03);
}}
.rank-badge {{
    position:absolute;
    left: 8px;
    top: 8px;
    background: linear-gradient(90deg,var(--accent),var(--accent-2));
    color: white;
    padding:6px 10px;
    font-weight:700;
    border-radius: 999px;
    font-size: 13px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.45);
}}
.basic {{
    margin-top: 8px;
}}
.name {{
    margin:6px 0 2px 0;
    font-size:18px;
}}
.meta {{ color: var(--muted); font-size:13px; }}

/* right side */
.card-right {{
    flex:1;
}}
.description {{
    margin-bottom: 10px;
    color: #dbeaf6;
    line-height:1.4;
}}
.stats-grid {{
    display:grid;
    grid-template-columns: repeat(5, 1fr);
    gap:8px;
    margin: 10px 0;
}}
.stat {{
    background: rgba(255,255,255,0.02);
    border-radius:8px;
    padding:8px;
    text-align:center;
    border: 1px solid rgba(255,255,255,0.02);
}}
.stat-name {{ font-size:11px; color:var(--muted); }}
.stat-value {{ font-weight:700; margin-top:4px; }}

/* bottom row */
.bottom-row {{
    display:flex;
    gap:16px;
    align-items:center;
    justify-content:space-between;
    margin-top:8px;
}}
.favor {{
    flex:1;
}}
.favor-label {{ font-size:13px; color:var(--muted); margin-bottom:6px; }}
.favor-bar {{
    height:10px;
    background: rgba(255,255,255,0.03);
    border-radius:999px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,0.02);
}}
.favor-fill {{
    height:100%;
    background: linear-gradient(90deg,var(--accent),var(--accent-2));
    width:0%;
}}
.record {{ color: var(--muted); font-size:13px; }}

/* subsections (skills/spells) */
.subsections {{
    display:flex;
    gap:12px;
    margin-top:12px;
    flex-wrap:wrap;
}}
.subsection {{
    min-width:160px;
    background: rgba(255,255,255,0.02);
    padding:8px;
    border-radius:8px;
    border:1px solid rgba(255,255,255,0.02);
}}
.subsection h4 {{
    margin:0 0 6px 0;
    font-size:13px;
}}
.kv-list .kv {{
    display:flex;
    justify-content:space-between;
    font-size:13px;
    margin-bottom:6px;
}}
.kv .k {{ color: var(--muted); }}
.kv .v {{ font-weight:600; }}

/* tiny helpers */
.empty {{ color: var(--muted); font-size:13px; font-style:italic; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <h1>Dragon Ladder</h1>
      <div class="subtitle">Ranked by position — top to bottom</div>
    </div>
    <div class="subtitle">Rendered: {safe(len(dragons_sorted))} dragons</div>
  </div>

  <div class="cards">
    {"".join(cards_html)}
  </div>
</div>

</body>
</html>
"""
    return full_html
