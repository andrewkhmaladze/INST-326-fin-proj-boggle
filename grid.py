import random
import string

def generate_grid(size=4):
    # Generate random uppercase letters A-Z
    letters = string.ascii_uppercase  # This will give all the letters from A-Z
    # Create a 2D list (size x size grid) of random letters
    grid = [[random.choice(letters) for _ in range(size)] for _ in range(size)]
    return grid

def print_grid(grid):
    # Print each row of the grid
    for row in grid:
        print(' '.join(row))


def load_dictionary(filename="wordList.txt"):
    # Open the dictionary file and read its words
    with open(filename, "r") as f:
        # Convert each word to uppercase and add to a set
        words = {line.strip().upper() for line in f}
    return words

def main():
    #Generate and print grid
    grid = generate_grid()
    print("Generated Boggle Grid:")
    print_grid(grid)
    
    #Load dictionary of words
    dictionary = load_dictionary("wordList.txt")
    print("\nLoaded Dictionary")
    print(dictionary)

if __name__ == "__main__":
    main()