import random

class RPS:
    def play(self):
        print("Welcome to Rock, Paper, Scissors!")

        choices = ['rock', 'paper', 'scissors']

        while True:
            player_choice = input("\nChoose ROCK, PAPER, or SCISSORS: ").lower()
            print(f"\nYou chose: {player_choice.upper()}")

            if player_choice in choices:
                break
            else:
                print("Invalid choice. Please choose another.")


        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice.upper()}")


        if player_choice == computer_choice:
            print("It's a tie!")
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'scissors' and computer_choice == 'paper') or \
             (player_choice == 'paper' and computer_choice == 'rock'):
            print("You win!")
        else:
            print("You lose!")

if __name__ == "__main__":
    game = RPS()
    game.play()