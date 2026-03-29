import random

def choose_difficulty():
    while True:
        print("\nChoose difficulty:")
        print("1. Easy (1–50, 10 attempts)")
        print("2. Medium (1–100, 7 attempts)")
        print("3. Hard (1–200, 5 attempts)")
        
        choice = input("Enter 1, 2, or 3: ")
        
        if choice == "1":
            return 50, 10
        elif choice == "2":
            return 100, 7
        elif choice == "3":
            return 200, 5
        else:
            print("Invalid choice. Try again.")

def play_game():
    print("🎯 Welcome to Guess My Number!")
    
    max_range, attempts = choose_difficulty()
    secret_number = random.randint(1, max_range)
    
    print(f"\nI have selected a number between 1 and {max_range}.")
    print(f"You have {attempts} attempts to guess it.\n")
    
    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"Attempt {attempt}: Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        if guess < secret_number:
            print("Too low! 📉")
        elif guess > secret_number:
            print("Too high! 📈")
        else:
            print(f"🎉 Correct! You guessed it in {attempt} attempts.")
            return
        
    print(f"\n❌ Game Over! The number was {secret_number}.")

def main():
    while True:
        play_game()
        again = input("\nDo you want to play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing! 👋")
            break

if __name__ == "__main__":
    main()
