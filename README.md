# **INST-326 Final Project: Boggle Game**

## **Project Description** 
This project is a completely functional Python Boggle game that relies on two players. It incorporates:
- A timer system
- A scoring system based on word count, with a total score calculated at the end
- Assignment of a winner based on scores
- A word-search logic that enables players to guess words in any adjacent cell
- A randomized 4x4 grid

---

## **Purpose of Each File**
- **`patchedWork3.py`**: The main file connecting all of the following files to run the game. User inputs are included to set the timer and guess words.
- **`grid.py`**: Generates a custom-made grid displaying random letters for players to guess.
- **`scoring.py`**: Manages scoring for each player based on valid words guessed, and determines the winner at the end.
- **`searchwords.py`**: Implements the logic to find valid words from the Boggle grid by navigating through each cell, allowing guesses in any adjacent direction. 
- **`timer.py`**: Handles the timer system, which is user-selected, to track each player's turn until the game ends.
- **`word-list.txt`**: A dictionary of all valid words used to verify player inputs.

---

## **How to Run the Program**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/andrewkhmaladze/INST-326-fin-proj-boggle.git
2. **Set the project directory:**
   ```bash
   cd INST-326-fin-proj-boggle
3. **Running the program:**
   ```bash
   python patchedWork3.py

## **How to Use the Program Correctly**
- Once the program is ran the player types in the seconds they want each turn to last
- Then both players must type "READY" to start the official game.
- The grid is generated and Player1 guesses words one at a time. The guesses must be:
     - Formed from adjacent cells in the grid
     - Valid words, otherwise it doesn't count towards the final score.
- Once the first turn timer runs out, Player2 repeats the last step
- Once that timer runs the game is officially done:
     - All Valid words available in the grid is displayed.
     - Both players total score is displayed.
     - A winner is determined from both scores!

