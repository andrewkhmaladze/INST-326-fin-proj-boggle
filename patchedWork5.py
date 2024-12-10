import random
import string
import time

def generate_grid(size=4):
    """ Creates 4x4 boggle grid

    Args: 
        size (int): value for the dimensions of the grid; default 4
        
    Returns:    
        grid (str): grid of random letters    
    """
    letters = string.ascii_uppercase
    grid = [[random.choice(letters) for _ in range(size)] for _ in range(size)]
    return grid

def print_grid(grid):
    """ Formats spaces in grid

    Args:   
        grid (str): randomized boggle grid 
        
    Side effects:
        Prints grid on console
    """ 
    for row in grid:
        print(' '.join(row))

def load_dictionary(filename="wordlist3.txt"):
    """opens word dictionary text file and stores words into list

    Arg:    
        filename (str): text file containing words for game
    
    Returns:
        words (list): word dictionary of valid words that can be found 
    """
    with open(filename, "r") as f:
        words = {line.strip().upper() for line in f}
    return words


def input_timer(prompt, timeout):
    """ runs timer during each player's turn
    
    Args:
        prompt (str): message for player when their turn starts
        timeout (int): number of seconds for each round
        
    Returns:    
        response (list): player's word responses    
        
    Side effects:
        Prints prompt and time on console
    """
    print(prompt)
    start_time = time.time()
    responses = []

    while time.time() - start_time <= timeout:
        remaining_time = timeout - (time.time() - start_time)
        if remaining_time <= 0:
            break
        print(f"Time left: {int(remaining_time)} seconds")
        user_input = input()
        responses.append(user_input.upper())

    print("Time's up")
    return responses

def searchwords(board, dictionary):
    """ looks for every word combination in grid that exists in words list
    
    Args: 
        board (str): boggle grid
        dictionary (list): words list of possible words
        
    Returns:
        found_words (set): all possible words that can be found with inputted grid     
    """
    rows, cols = len(board), len(board[0])

    # create a set of prefixes from the dictionary
    prefixes = set()
    for word in dictionary:
        for i in range(1, len(word) + 1):
            prefixes.add(word[:i])

    found_words = set()

    def dfs(x, y, current_word, visited):
        """ Depth-first search helper function used to make sure every letter path has been 
            visited to make every word possible
            
        Args:
            x (int): x-coordinate of grid
            y (int): y-coordinate of grid
            current_word (str): 
            visited (stack): visited letters
        """
        # stop process if out of bounds/cell scanned 
        if x < 0 or x >= rows or y < 0 or y >= cols or (x, y) in visited:
            return
        current_word += board[x][y]
        if current_word not in prefixes:
            return
        if current_word in dictionary:
            found_words.add(current_word)
        visited.add((x, y))
        # explore all directional movements of grid location 
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            dfs(x + dx, y + dy, current_word, visited)
        visited.remove((x, y))

    # for every cell in grid
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, '', set())

    return found_words

class Player:
    """
    Represents a player for the Boggle game.

    Attributes:
        name (str): Name of the player
        player_words (set): Guessed words by the player in a set.
    """
    def __init__(self, name, responses):
        """
        Initializes a Player object with a name and their guessed words.

        Args:
            name (str): Player name.
            responses (list): Guessed words by the player in a list.
        """
        self.name = name
        self.player_words = set(responses)

    def points(self, dictionary, valid_words_from_grid):
        """
        Calculates the player's score based on the valid words guessed and length

        Side Effects:
            Changes the self.player_words by removing all invalid words
        
        Args:
            dictionary (set): Valid words from the dictionary in a set.
            valid_words_from_grid (set): All valid words found in a set

        Returns:
            int: The total score for the player.
        """
        points = 0
        # store valid words in both dictionary/grid
        valid_words = {
            word for word in self.player_words if word in dictionary and word in valid_words_from_grid
        }
        self.player_words = valid_words
        # length-based scoring 
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
    """
    Displays all valid words from the grid, the scores of each player, and announces the winner.

    Side Effects: 
        Changes both player1.player_words and player2.player_words in order to remove shared guessed words.
    
    Args:
        player1 (Player): The first player object.
        player2 (Player): The second player object.
        dictionary (set): The set of valid words from the dictionary.
        valid_words_from_grid (set): The set of valid words found in the grid.

    Returns:
        None
    """
    # Avoid duplication 
    shared_words = player1.player_words.intersection(player2.player_words)
    player1.player_words -= shared_words
    player2.player_words -= shared_words
    
    p1_score = player1.points(dictionary, valid_words_from_grid)
    p2_score = player2.points(dictionary, valid_words_from_grid)

    print(f"{player1.name}'s total points: {p1_score}")
    print(f"{player2.name}'s total points: {p2_score}")
    if p1_score > p2_score:
        print(f"Congratulations {player1.name} is the winner!")
    elif p2_score > p1_score:
        print(f"Congratulations {player2.name} is the winner!")
    else:
        print("It's a tie!")

def setup_game():
    """
    Asks the user for a custom time for turn duration, and starts the game by confirming readiness
    from each player.

    Side Effects:
        Reads all the inputs from user in the console.

    Returns:
        int: Turn time in seconds.
    """
    while True:
        try:
            # Query user on seconds per turn 
            turn_time = int(input(" How many seconds do you want each turn to last? "))
            if turn_time <= 0:
                print("Enter a positive number of seconds")
            else:
                break
        except ValueError:
            print("Invalid input")

    print(f"Each turn will last {turn_time} seconds")
    print("\nBoth players must type 'READY' to start the game")

    player1_ready = False
    player2_ready = False
    # while loop until both are ready 
    while not (player1_ready and player2_ready):
        player1_response = input("Player 1, type 'READY' when you are ready: ").strip()
        player2_response = input("Player 2, type 'READY' when you are ready: ").strip()

        if player1_response.upper() == "READY":
            player1_ready = True
        else:
            print("Player 1 is not ready")

        if player2_response.upper() == "READY":
            player2_ready = True
        else:
            print("Player 2 is not ready")

    print("\nBoth players ready")
    return turn_time

def main():
    """
    The main function to run the Boggle game. Sets the game up, gathers all the user inputs for timer and readiness, 
    generates the grid, calculates scores, and announces the winner.

    Returns:
        None
    """
    # setup game 
    turn_time = setup_game()

    # Generate and display grid
    grid = generate_grid()
    print("\nBoggle Grid:")
    print_grid(grid)

    # Load dictionary of valid words
    dictionary = load_dictionary("wordlist3.txt")

    # Player 1's turn
    print("\nPlayer 1 turn:")
    player1_words = input_timer("Enter words one at a time:", timeout=turn_time)

    # Player 2's turn
    print("\nPlayer 2 turn:")
    player2_words = input_timer("Enter words one at a time:", timeout=turn_time)

    # Call searchwords
    valid_words = searchwords(grid, dictionary)
    print("\nWords found in the grid:")
    print(valid_words)

    # Create player objects + score 
    player1 = Player("Player 1", player1_words)
    player2 = Player("Player 2", player2_words)
    result(player1, player2, dictionary, valid_words)

if __name__ == "__main__":
    main()
