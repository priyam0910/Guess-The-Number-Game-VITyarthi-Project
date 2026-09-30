# database.py
import json
import os
import Settings

def load_game_data():
    if os.path.exists(Settings.SAVE_FILE):
        try:
            with open(Settings.SAVE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Save file looks corrupted. Starting fresh...")
            return {}
    return {}

def save_game_data(db):
    with open(Settings.SAVE_FILE, "w") as f:
        json.dump(db, f, indent=4)

def setup_player(db, name):
    if name not in db:
        db[name] = {
            "games_played": 0,
            "wins": 0,
            "total_score": 0,
            "achievements": [],
            "best_scores": {
                "easy": None,
                "medium": None,
                "hard": None,
                "extreme": None,
                "nightmare": None
            }
        }
    else:
        # Patching old profiles so they don't break
        player = db[name]
        if "achievements" not in player:
            player["achievements"] = []
        if "best_scores" not in player:
            player["best_scores"] = {
                "easy": player.get("best_easy"), 
                "medium": None,
                "hard": player.get("best_hard"),
                "extreme": None,
                "nightmare": None
            }
        if "total_score" not in player:
            player["total_score"] = 0
            
    return db