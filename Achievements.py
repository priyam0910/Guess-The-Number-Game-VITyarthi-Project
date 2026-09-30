# achievements.py
import time
import Settings

def evaluate_achievements(player_name, db, mode_name, attempts, hints_used):
    stats = db[player_name]
    newly_unlocked = []
    
    def grant(key):
        if key not in stats["achievements"]:
            stats["achievements"].append(key)
            newly_unlocked.append(key)

    if stats["wins"] == 1:
        grant("first_blood")
        
    if stats["games_played"] >= 25:
        grant("veteran")
        
    if stats.get("total_score", 0) >= 5000:
        grant("high_roller")
        
    if attempts == 1:
        grant("flawless")
        
    if mode_name.lower() == "nightmare":
        grant("nightmare_slayer")
        
    if mode_name.lower() in ["hard", "extreme", "nightmare"] and hints_used == 0:
        grant("no_help_needed")
        
    for badge in newly_unlocked:
        title, desc = Settings.ACHIEVEMENTS[badge]
        print(f"\n🌟 ACHIEVEMENT UNLOCKED: {title} 🌟")
        print(f"   -> {desc}")
        time.sleep(1.5)