
class Player:
    def __init__(self, name, responses):
        self.name = name
        self.player_words = set(responses) #comes from user inputs
        
    def points(self, dictionary):
        points = 0 
        for word in self.player_words:
            # checks if word in dictionary
            if word not in dictionary:
                self.player_words.remove(word)
            
            # adding points
            if len(word) == 3 or len(word) == 4:
                points += 1
            if len(word) == 5:
                points += 2
            if len(word) == 6:
                points += 3
            if len(word) == 7:
                points += 5
            if len(word) >= 8:
                points += 11
                
        return points
            
    
def result(player1, player2):
    # finds words both players used
    shared_words = player1.player_words.intersection(player2.player_words)
    
    # removes shared words since neither player gets points for those
    for word in shared_words:
        player1.player_words.remove(word)
        player2.player_words.remove(word)

    # prints players' scores and game winner
    print(f"{player1.name}'s total points: {player1.points}")
    print(f"{player2.name}'s total points: {player2.points}")
    if player1.points > player2.points:
        print(f"Congratulations {player1.name} is the winner!")
    else:
        print(f"Congratulations {player2.name} is the winner!")
    
    
    
        
        
        
        