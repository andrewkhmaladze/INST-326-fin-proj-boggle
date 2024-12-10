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
    """ looks for every word combination in grid that exists in words dictionary 
        text file
    
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
            current_word (str): current word that's being searched in grid
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

    def points(self, valid_words_from_grid):
        """
        Calculates the player's score based on the valid words guessed and length

        Side Effects:
            Changes the self.player_words by removing all invalid words
        
        Args:
            valid_words_from_grid (set): All valid words found in a set

        Returns:
            int: The total score for the player.
        """
        points = 0
        # checks and stores player's responses that are in word directionary and grid
        player_valid_words = {
            word for word in self.player_words if word in valid_words_from_grid
        }
        self.player_words = player_valid_words
        # length-based scoring 
        for word in player_valid_words:
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

def result(player1, player2, valid_words_from_grid):
    """
    Displays each player's valid words from the grid, the scores of each player, and announces the winner.

    Side Effects: 
        Changes both player1.player_words and player2.player_words in order to remove shared guessed words.
        Prints on messages about players scores on console
    
    Args:
        player1 (Player): The first player object.
        player2 (Player): The second player object.
        dictionary (list): The list of words from the dictionary text file.
        valid_words_from_grid (set): The set of all possible valid words found in the grid.
    """
    # removes shared since players don't get points for those
    shared_words = player1.player_words.intersection(player2.player_words)
    player1.player_words -= shared_words
    player2.player_words -= shared_words
    
    p1_score = player1.points(valid_words_from_grid)
    p2_score = player2.points(valid_words_from_grid)

    # Printing game outcome 
    print(f"\nWords {player1.name} found: {player1.player_words}")
    print(f"Words {player2.name} found: {player2.player_words}")
    if len(shared_words) != 0:
        print(f"Shared words removed: {shared_words}")
        
    print(f"\n{player1.name}'s total points: {p1_score}")
    print(f"{player2.name}'s total points: {p2_score}")

    if p1_score > p2_score:
        print(f"Congratulations {player1.name} is the winner!!")
    elif p2_score > p1_score:
        print(f"Congratulations {player2.name} is the winner!!")
    else:
        print("It's a tie!!")

def setup_game(p1_name, p2_name):
    """
    Asks the user for a custom time for turn duration, and starts the game by confirming readiness
    from each player.

    Args:
        p1_name: Player 1's name
        p2_name: Player 2's name
    
    Side Effects:
        Reads all the inputs from user in the console.
        
    Raises:
        ValueError: player didn't input integer value for time

    Returns:
        int: Turn time in seconds.
    """
    while True:
        try:
            # Query user on seconds per turn 
            turn_time = int(input("How many seconds do you want each turn to last? "))
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
        player1_response = input(f"{p1_name}, type 'READY' when you are ready: ").strip()
        player2_response = input(f"{p2_name}, type 'READY' when you are ready: ").strip()

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
    print("Welcome to Boggle!")
    player1_name = input("Type Player 1's name: ").strip()
    player2_name = input("Type Player 2's name: ").strip()
    turn_time = setup_game(player1_name, player2_name)

    # Load dictionary of valid words for game from text file
    dictionary = load_dictionary("wordlist3.txt")

    # Generate and display grid
    grid = generate_grid()
    print("\nBoggle Grid:")
    print_grid(grid)

    # Player 1's turn
    print(f"\n{player1_name}'s turn")
    player1_words = input_timer("Enter words one at a time:", timeout=turn_time)

    # Player 2's turn
    print(f"\n{player2_name} turn:")
    player2_words = input_timer("Enter words one at a time:", timeout=turn_time)

    # Call searchwords to find valid words for this round's grid
    valid_words = searchwords(grid, dictionary)
    print("\nAll possible words found in the grid:")
    print(valid_words)

    # Create player objects + score 
    player1 = Player(player1_name, player1_words)
    player2 = Player(player2_name, player2_words)
    result(player1, player2, valid_words)

if __name__ == "__main__":
    main()
