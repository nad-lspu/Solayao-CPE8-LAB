import random

class RPS_Game:
    def __init__(self):
        self.choices = ['rock', 'paper', 'scissors']

    def get_computer_choice(self):
        return random.choice(self.choices)

    def get_player_choice(self):
        player_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        if player_choice in self.choices:
            return player_choice
        else:
            print("Invalid choice. Please try again.")

    def determine_winner(self, player_choice, computer_choice):
        if player_choice == computer_choice:
            return "It's a tie!"
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'paper' and computer_choice == 'rock') or \
             (player_choice == 'scissors' and computer_choice == 'paper'):
            return "You win!"
        else:
            return "You Lose!"

    def play_RPS(self):
        print("Welcome to Rock, Paper, Scissors!")
        player_choice = self.get_player_choice()
        computer_choice = self.get_computer_choice()
        print(f"\nYou chose: {player_choice}")
        print(f"Computer chose: {computer_choice}")
        result = self.determine_winner(player_choice, computer_choice)
        print(result)

if __name__ == "__main__":
    game = RPS_Game()
    game.play_RPS()