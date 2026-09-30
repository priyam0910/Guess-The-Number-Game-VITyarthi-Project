# main.py
import Assets
import Database
import Menus

def main():
    db = Database.load_game_data()
    
    print(Assets.TITLE_ART)
    
    current_player = input("Enter your name to start: ").strip().capitalize()
    if not current_player:
        current_player = "Guest"
        
    db = Database.setup_player(db, current_player)
    Database.save_game_data(db)
    
    print(f"\nWelcome in, {current_player}.")
    
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Play Game")
        print("2. Leaderboard")
        print("3. My Profile")
        print("4. Quit")
        
        choice = input("> ").strip()
        
        if choice == '1':
            Menus.difficulty_select(current_player, db)
        elif choice == '2':
            Menus.display_leaderboard(db)
        elif choice == '3':
            current_player = Menus.view_profile(current_player, db)
        elif choice == '4':
            print(Assets.QUIT_ART)
            print(f"\nCatch you later, {current_player}!\n")
            break
        else:
            print("Nope, type 1, 2, 3, or 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Assets.QUIT_ART)
        print("\n\nGame closed forcefully. See ya!")