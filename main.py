import time
from grid import generate_grid, print_grid, load_dictionary
from scoring import Player
from searchwords import searchwords
from timer import input_timer


def main():
    # Loads the wordlist
    dictionary = load_dictionary(r"C:\Users\aiink\OneDrive\Documents\Inst326\FinalProject\wordList.txt")
    print("Dictionary loaded successfully.")

    # Generates a grid if there is only valid words inside of it.
    valid_words = set()
    grid = None
    while not valid_words:
        grid_size = 4
        grid = generate_grid(grid_size)
        print("\nGenerated Boggle Grid:")
        print_grid(grid)
        valid_words = searchwords(grid, dictionary)
        if not valid_words:
            print("No valid words found in the grid. Regenerating...")

    # Hide valid words during gameplay
    print(f"\nValid words from the grid (hidden during play): {valid_words}")  # Debugging only

    # Starts the input and lets the users input
    print("\nThe game starts now! You have 30 seconds to find as many words as possible.")
    player1_responses = input_timer("Player 1, enter words (press Enter after each word): ", timeout=30)
    print("\nTime's up!")

    
    player1_responses = [response.upper() for response in player1_responses]

    # Player scoring
    player1 = Player("Player 1", player1_responses)
    player1_score = player1.points(valid_words)

    # Display all the results
    print(f"\nPlayer 1's total score: {player1_score}")
    print(f"Words you found: {player1.player_words}")
    print(f"Invalid words removed: {set(player1_responses) - player1.player_words}")

    
    invalid_words = set(player1_responses) - player1.player_words
    for word in invalid_words:
        if word not in valid_words:
            print(f"'{word}' is not valid based on the grid.")
        elif word not in dictionary:
            print(f"'{word}' is not in the dictionary.")

if __name__ == "__main__":
    main()
