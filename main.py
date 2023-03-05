from game import Game
from service_game import ServiceGame

if __name__ == '__main__':
    while True:
        Game.show_menu()
        choice = input("Choose an item: ")
        if choice == '1':
            game = Game()
            game.play()
        elif choice == '2':
            service_game = ServiceGame()
            name = input("Enter the player's name: ")
            statistics = service_game.get_player_statistics(name)
            games = service_game.get_player_last_games(name)
            Game.show_player_statistics(statistics, games)
        elif choice == "0":
            break
        else:
            print("Invalid menu item")
