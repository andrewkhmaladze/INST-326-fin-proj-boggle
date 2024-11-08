def searchwords(board, dictionary):
    
    rows, cols = len(board), len(board[0])
    
    # Creates a set for all prefixes that can be created from the words.
    prefix_set = set()
    
    for word in dictionary:
        for i in range(1, len(word) + 1):
            prefix_set.add(word[:i])

    # Creates a set for all the valid words that are found.
    found_words = set()

    # The Depth-first search function used to search for all the words
    def dfs(x, y, current_word, visited):
        #Verifies both the words boundary within the grid, and also if it's been visited
        if (x < 0 or x >= rows or y < 0 or y >= cols):
            return
        if (x, y) in visited:
            return
        # Adds the letter
        current_word += board[x][y]
        if current_word not in prefix_set:
            return
        if current_word in dictionary:
            found_words.add(current_word)
        # Sets a mark that it's already been visited
        visited.add((x, y))
        # Explores every cell that is adjacent
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    dfs(x + dx, y + dy, current_word, visited)
        visited.remove((x, y))

    # Loops through every cell, and uses the dfs function to find all the words
    for i in range(rows):
        for j in range(cols):
            dfs(i, j, '', set())

    return found_words

# Test grid for logic
board = [
    ['B', 'A', 'T', 'E'],
    ['O', 'S', 'I', 'R'],
    ['L', 'N', 'C', 'A'],
    ['G', 'T', 'H', 'E']
]

dictionary = ['BAT','BASE','SIRE','RICE','BOLT','SING','HEART','COAT','SHORE','LACE']


found_words = searchwords(board, dictionary)
print("Words found:", found_words)


