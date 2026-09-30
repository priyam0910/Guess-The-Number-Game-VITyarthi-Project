# menus.py
import Assets
import Settings
import Database
import Gameplay

def difficulty_select(player_name, db):
    while True:
        print("\n--- SELECT DIFFICULTY ---")
        print("1. Easy      (1-50,   10 tries)")
        print("2. Medium    (1-100,   7 tries)")
        print("3. Hard      (1-200,   5 tries)")
        print("4. Extreme   (1-500,   5 tries)")
        print("5. Nightmare (1-1000,  4 tries)")
        print("6. Custom    (Set your own rules)")
        print("7. Back to Main Menu")
        
        choice = input("> ").strip()
        
        if choice == '1':
            Gameplay.run_round(player_name, db, 50, 10, "Easy", Assets.EASY_ART)
            break
        elif choice == '2':
            Gameplay.run_round(player_name, db, 100, 7, "Medium", Assets.MEDIUM_ART)
            break
        elif choice == '3':
            Gameplay.run_round(player_name, db, 200, 5, "Hard", Assets.HARD_ART)
            break
        elif choice == '4':
            Gameplay.run_round(player_name, db, 500, 5, "Extreme", Assets.EXTREME_ART)
            break
        elif choice == '5':
            Gameplay.run_round(player_name, db, 1000, 4, "Nightmare", Assets.NIGHTMARE_ART)
            break
        elif choice == '6':
            print(Assets.CUSTOM_ART)
            print("\n-- Custom Rules --")
            try:
                high = int(input("Max number (e.g., 5000): "))
                tries = int(input("How many attempts?: "))
                if high < 2 or tries < 1:
                    print("Numbers too low to make a real game.")
                    continue
                Gameplay.run_round(player_name, db, high, tries, "Custom", Assets.CUSTOM_ART)
                break
            except ValueError:
                print("Letters don't work here. Need actual numbers.")
        elif choice == '7':
            return
        else:
            print("Not a valid option.")

def display_leaderboard(db):
    print(Assets.LEADERBOARD_ART)
    
    if not db:
        print("\nNo players found. Go play a game first!")
        input("\nPress Enter...")
        return
        
    print("\n--- GLOBAL LEADERBOARD ---")
    
    sorted_players = sorted(
        db.items(), 
        key=lambda x: x[1].get("total_score", 0), 
        reverse=True
    )
    
    print(f"{'Rank':<5} | {'Player':<15} | {'Score':<8} | {'Wins':<5} | {'Win %'}")
    print("-" * 55)
    
    for i, (name, stats) in enumerate(sorted_players, 1):
        score = stats.get("total_score", 0)
        wins = stats.get("wins", 0)
        played = stats.get("games_played", 0)
        
        win_rate = (wins / played * 100) if played > 0 else 0
        
        clean_name = name[:12] + "..." if len(name) > 15 else name
        
        print(f"#{i:<4} | {clean_name:<15} | {score:<8} | {wins:<5} | {win_rate:.1f}%")
        
    print("-" * 55)
    input("\nPress Enter to go back...")

def view_profile(player_name, db):
    while True:
        print(Assets.PROFILE_ART)
        print(f"\n--- PROFILE: {player_name.upper()} ---")
        print("1. View My Stats")
        print("2. View My Badges/Achievements")
        print("3. Switch Player")
        print("4. Back to Main Menu")
        
        choice = input("> ").strip()
        
        if choice == '1':
            stats = db[player_name]
            print(f"\n--- {player_name}'s Lifetime Stats ---")
            print(f"Total Points: {stats.get('total_score', 0):,}")
            print(f"Games Played: {stats['games_played']}")
            print(f"Total Wins:   {stats['wins']}")
            
            wr = (stats['wins'] / stats['games_played'] * 100) if stats['games_played'] > 0 else 0
            print(f"Win Rate:     {wr:.1f}%")
            
            print("\n-- Personal Bests --")
            for mode, best in stats.get("best_scores", {}).items():
                display = best if best is not None else "Unbeaten"
                print(f" {mode.capitalize():<10}: {display}")
            input("\nPress Enter...")
            
        elif choice == '2':
            print(f"\n--- {player_name}'s Trophy Case ---")
            badges = db[player_name].get("achievements", [])
            
            if not badges:
                print("Pretty empty in here. Keep playing!")
            else:
                for badge in badges:
                    title, desc = Settings.ACHIEVEMENTS[badge]
                    print(f"🏅 {title}: {desc}")
            input("\nPress Enter...")
            
        elif choice == '3':
            new_user = input("\nEnter new player name: ").strip().capitalize()
            if new_user:
                player_name = new_user
                db = Database.setup_player(db, player_name)
                Database.save_game_data(db)
                print(f"Swapped to {player_name}.")
                return player_name
            else:
                print("Name can't be blank.")
                
        elif choice == '4':
            return player_name
            
        else:
            print("Invalid choice.")