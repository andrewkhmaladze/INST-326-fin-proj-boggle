import random
import string
from inputimeout import inputimeout, TimeoutOccurred
import time

# create the Boggle grid with random letters
def generate_grid(size=4):
    letters = string.ascii_uppercase
    grid = [[random.choice(letters) for _ in range(size)] for _ in range(size)]
    return grid

# print the grid in a clear format
def print_grid(grid):
    for row in grid:
        print(' '.join(row))

#load valid words from a dictionary file
def load_dictionary(filename="wordList.txt"):
    with open(filename, "r") as f:
        words = {line.strip().upper() for line in f}
    return words

# let players enter words with a timer
def input_timer(prompt, timeout=60):
    print(prompt)
    start_time = time.time()
    responses = []

    while time.time() - start_time <= timeout:
        try:
            # get player input with timeout
            user_input = inputimeout(prompt='', timeout=timeout - (time.time() - start_time))
            responses.append(user_input.upper())
        except TimeoutOccurred:
            # stop when time runs out
            print("\nout of time")
            break

    return responses

#find valid words in the grid based on dictionary
def searchwords(board, dictionary):
    rows, cols = len(board), len(board[0])

    #create a set of all valid prefixes from the dictionary
    prefixes = set()
    for word in dictionary:
        for i in range(1, len(word) + 1):
            prefixes.add(word[:i])

    found_words = set()

    # helper function to search the grid 
    def dfs(x, y, current_word, visited):
        # stop if out of bounds or cell already visited
        if x < 0 or x >= rows or y < 0 or y >= cols or (x, y) in visited:
            return
        current_word += board[x][y]
        # stop if the word doesn't match any prefix
        if current_word not in prefixes:
            return
        # add the word if it's valid
        if current_word in dictionary:
            found_words.add(current_word)
        visited.add((x, y))
        # explore 8 directions
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            dfs(x + dx, y + dy, current_word, visited)
        visited.remove((x, y))

    # start helper function from every cell in the grid
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, '', set())

    return found_words


class Player:
    def __init__(self, name, responses):
        self.name = name
        self.player_words = set(responses)

    def points(self, dictionary, valid_words_from_grid):
        points = 0
        #keep only valid words in both dictionary and grid
        valid_words = {
            word for word in self.player_words if word in dictionary and word in valid_words_from_grid
        }
        self.player_words = valid_words
        # score words on length
        for word in valid_words:
            if len(word) == 3 or len(word) == 4:
                points += 1
            elif len(word) == 5:
                points += 2
            elif len(word) == 6:
                points += 3
            elif len(word) == 7:
                points += 5
            elif len(word) >= 8:
                points += 11
        return points


def result(player1, player2, dictionary, valid_words_from_grid):
    #Remove shared words to avoid duplicate scoring
    shared_words = player1.player_words.intersection(player2.player_words)
    player1.player_words -= shared_words
    player2.player_words -= shared_words

    # calculate scores
    p1_score = player1.points(dictionary, valid_words_from_grid)
    p2_score = player2.points(dictionary, valid_words_from_grid)

    # print scores and winner
    print(f"{player1.name}'s total points: {p1_score}")
    print(f"{player2.name}'s total points: {p2_score}")
    if p1_score > p2_score:
        print(f"Congratulations {player1.name} is the winner!")
    elif p2_score > p1_score:
        print(f"Congratulations {player2.name} is the winner!")
    else:
        print("It's a tie!")


def main():
    #generate/display grid
    grid = generate_grid()
    print("Boggle Grid:")
    print_grid(grid)

    # load dictionary of valid words
    dictionary = load_dictionary("wordList.txt")

    # player 1's turn 
    print("\nPlayer 1 turn:")
    player1_words = input_timer("Enter words one at a time:", timeout=60)

    # player 2's turn 
    print("\nPlayer 2 turn:")
    player2_words = input_timer("Enter words one at a time:", timeout=60)

    # find all valid words in grid
    valid_words = searchwords(grid, dictionary)
    print("\nWords found in the grid:")
    print(valid_words)

    # create player objects/calculate results
    player1 = Player("Player 1", player1_words)
    player2 = Player("Player 2", player2_words)
    result(player1, player2, dictionary, valid_words)

if __name__ == "__main__":
    main()