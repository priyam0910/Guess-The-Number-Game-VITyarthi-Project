# gameplay.py
import random
import Assets
import Settings
import Database
import Achievements

def run_round(player_name, db, upper_bound, max_attempts, mode_name, art_asset):
    print(art_asset)
    print(f"\n--- {mode_name.upper()} MODE ---")
    
    secret = random.randint(1, upper_bound)
    attempts = 0
    guesses = []
    
    hints_allowed = 2
    hints_used = 0
    
    base_pts = 100 * (upper_bound // 50) 
    
    print(f"Target: 1 to {upper_bound}.")
    print(f"Attempts: {max_attempts}.")
    print(f"Need help? Type 'hint' (costs points!).\n")
    
    while attempts < max_attempts:
        if guesses:
            print(f"History: {', '.join(map(str, guesses))}")
            
        raw_input = input(f"[{attempts + 1}/{max_attempts}] Your guess: ").strip().lower()
        
        if raw_input == 'hint':
            if hints_used >= hints_allowed:
                print("No hints left! You're on your own.\n")
                continue
                
            hints_used += 1
            print(f"\n--- HINT {hints_used} ---")
            
            if hints_used == 1:
                parity = "EVEN" if secret % 2 == 0 else "ODD"
                print(f"💡 The number is {parity}.")
            elif hints_used == 2:
                div = random.choice([3, 4, 5, 7, 10])
                if secret % div == 0:
                    print(f"💡 The number IS a multiple of {div}.")
                else:
                    print(f"💡 The number is NOT a multiple of {div}.")
            print("-" * 15 + "\n")
            continue
        
        try:
            guess = int(raw_input)
        except ValueError:
            print("Come on, that's not a number. Try again.\n")
            continue
            
        if guess in guesses:
            print("You already tried that one! I won't count it.\n")
            continue
            
        guesses.append(guess)
        attempts += 1
        
        if guess == secret:
            print(Assets.WIN_ART)
            print(f"Spot on! You got it in {attempts} tries.")
            
            multiplier = (max_attempts - attempts) + 1 
            earned = base_pts * multiplier
            
            if hints_used > 0:
                penalty = int(earned * (0.25 * hints_used))
                earned -= penalty
                print(f"Hint penalty applied: -{penalty} pts")
                
            db[player_name]["total_score"] += earned
            print(f"Score Awarded: {earned} pts (Multiplier: {multiplier}x)\n")
            
            db[player_name]["games_played"] += 1
            db[player_name]["wins"] += 1
            
            safe_mode = mode_name.lower()
            if safe_mode in db[player_name]["best_scores"]:
                current_best = db[player_name]["best_scores"][safe_mode]
                if current_best is None or attempts < current_best:
                    db[player_name]["best_scores"][safe_mode] = attempts
                    print(f"🎉 NEW PERSONAL BEST FOR {mode_name.upper()}! 🎉\n")
            
            Achievements.evaluate_achievements(player_name, db, mode_name, attempts, hints_used)
            Database.save_game_data(db)
            
            input("Press Enter to head back...")
            return
            
        if guess < secret:
            print("📉 Too low!")
        else:
            print("📈 Too high!")
            
        if attempts < max_attempts and random.random() < 0.35:
            if random.choice([True, False]):
                print(f"💬 {random.choice(Settings.MOTIVATIONAL)}\n")
            else:
                print(f"😈 {random.choice(Settings.DEMOTIVATIONAL)}\n")
        else:
            print() 
            
    print(Assets.LOSE_ART)
    print(f"Out of tries, {player_name}.")
    print(f"The number I was thinking of was {secret}.")
    
    db[player_name]["games_played"] += 1
    Database.save_game_data(db)
    input("\nPress Enter to walk away in shame...")