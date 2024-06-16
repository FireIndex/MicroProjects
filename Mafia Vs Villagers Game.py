import random
import sys
from typing import List, Optional

# INSIGHTS:
# Always villager will die min(number of mafia members, number of villagers) times.
# Winning Conditions:
    # Villagers Win: If all mafia members are eliminated.
    # Mafia Wins: If all villagers are eliminated.
# Mafia Rules:
    # Mafia members are prohibited from voting to eliminate or killing each other.
    # Mafia members should not outnumber the villagers to maintain game balance and fairness. (should len of mafia < len of villager)
 

class Player:
    """Represents a player in the Mafia game."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.vote: Optional[str] = None

    def __str__(self) -> str:
        return self.name


class MafiaGame:
    """Implements the Mafia game logic."""

    def __init__(self, auto_start: bool = False) -> None:
        self.players: List[Player] = []  # List of all players
        self.mafia: List[Player] = []    # List of mafia members
        self.dead: List[Player] = []     # List of dead players
        self.winner: Optional[str] = None
        self.auto_start = auto_start

    def add_player(self, player: Player) -> None:
        """Adds a player to the game."""
        self.players.append(player)

    def add_mafia(self, player: Player) -> None:
        """Designates a player as a mafia member."""
        self.mafia.append(player)

    def kill(self, player: Player, through_vote: bool = False) -> None:
        """Kills a player, either by vote or by mafia action."""
        self.dead.append(player)
        is_mafia = player in self.mafia

        if is_mafia:
            self.mafia.remove(player)
        self.players.remove(player)

        if through_vote:
            role = "🎭 mafia" if is_mafia else "😵 villager"
            print(f"😊 villager killed {player.name}, who was a {role}!") # f"😊 {player.name} was a {role}!"
        else:
            print(f"🎭 -> 😵 Mafia killed {player.name}!") # f"🎭 -> 😵 {player.name} was killed!"

    def check_winner(self) -> None:
        """Checks if there's a winner."""
        only_villagers = [player for player in self.players if player not in self.mafia]
        if len(self.mafia) == 0:
            self.winner = "😊 Villagers"
        elif len(only_villagers) == 0:
            self.winner = "🎭 Mafia"
        else:
            self.winner = None

    def draw_line(self, char: str = "=", length: int = 30) -> str:
        """Returns a line of characters for formatting."""
        return char * length

    def play(self) -> None:
        """Executes the game loop until a winner is determined."""
        print(f"Players: {', '.join(player.name for player in self.players)}\n")
        print(f"{self.draw_line('-', 10)} 🎭 Game Started! {self.draw_line('-', 10)}\n")

        while not self.winner:
            # Mafia kills a random villager
            victim = self.choose_victim()
            self.kill(victim, through_vote=False)

            self.check_winner()
            if self.winner:
                print()
                break  # Skip voting if the game is over

            # Villagers vote to eliminate a player
            player_to_vote = self.vote_out_player()
            self.kill(player_to_vote, through_vote=True)
            print()

            self.check_winner()

        # Announce game over and winners
        self.announce_winner()

    def choose_victim(self) -> Player:
        """Chooses a victim for the mafia to kill."""
        victim = None
        while not victim:
            victim = random.choice(self.players)
            if victim in self.mafia:  # Mafia cannot kill another mafia
                victim = None
        return victim

    def vote_out_player(self) -> Player:
        """Handles the voting process to eliminate a player."""
        player_to_vote = None
        if self.auto_start:
            player_to_vote = random.choice(self.players)
        else:
            print(f"Players left to vote: {', '.join(player.name for player in self.players)}")
            while not player_to_vote:
                player_name = input("Enter the name of the player you want to vote out: ").strip().lower()
                if player_name == "exit":
                    sys.exit()
                player_to_vote = next((player for player in self.players if player.name.lower() == player_name), None)
                if not player_to_vote:
                    print("Player not found. Please try again.")
        return player_to_vote

    def announce_winner(self) -> None:
        """Announces the game over and winners."""
        print(f"{self.draw_line('-', 10)} 🎭 Game Over! {self.draw_line('-', 10)}\n")
        print("Remaining -")
        print(f"🎭 Mafia members: {', '.join(mafia.name for mafia in self.mafia)}")
        print(f"😊 Villagers: {', '.join(player.name for player in self.players if player not in self.mafia)}\n")
        print(f"The {self.winner} have won the game!")


def main(auto_start: bool, Player: List[Player], num_mafia: int) -> None:
    """Main function to initialize and start the game."""
    game = MafiaGame(auto_start=auto_start)

    # Add players to the game
    for player in players:
        game.add_player(player)

    # Randomly assign three mafia members
    while len(game.mafia) != num_mafia:
        player = random.choice(players)
        if player not in game.mafia:
            game.add_mafia(player)

    # Start the game
    print(f"\n{game.draw_line()} 🎭 Mafia Game {game.draw_line()}\n")
    game.play()


if __name__ == "__main__":
    players = [
        Player("Alice"), Player("Bob"), Player("Charlie"), Player("David"),
        Player("Eve"), Player("M3GAN"), Player("Frank"), Player("Grace"),
        Player("Wanda"), Player("Thora")
    ]

    num_mafia = int(input(f"Enter the number of mafia members out of {len(players)} ({int(len(players)*0.3)} recommended): "))
    if num_mafia < 1 or num_mafia >= len(players):
        print("Invalid number of mafia members. Exiting...")
        sys.exit()

    while True:
        start_mode = input("Do you want to play again? ay:auto_run, my:manual_run or exit: ").strip().lower()
        if start_mode == "exit":
            break
        auto_start = start_mode == "ay"
        main(auto_start, players, num_mafia)
        print()
