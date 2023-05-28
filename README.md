AI Connect Four – Minimax vs Evolutionary Algorithms
Zuhair Arif 24504 - - Danish Raza 24796 - - Zarlish Mohtashem 24452

This project contains a Connect Four game where you can play against two different types of artificial intelligence: a traditional Minimax algorithm with alpha-beta pruning, and an Evolutionary Algorithm (EA).
Getting Started
These instructions will get you a copy of the project up and running on your local machine.
Prerequisites
You will need to have Python installed on your computer. If you don't have Python installed you can download it here.
Running the Game
This project contains two modes of play, which are described below:
1.	AI versus AI
To test Evolutionary Algorithms against Minimax using alpha-beta pruning, run the AI_V_AI.py program. When the program runs, you will be asked to enter a number between 1 and 5. This number sets the difficulty (depth) of alpha-beta pruning.
The scores of the AI players will be automatically stored in the winning_data.pickle file after each game. To view the output, run the DataWriter.py program, which will read the pickle file and write the data into the data.txt file.
2.	User versus AI
To play against AI, run the User_VS_AI.py file. Once the program is running, you will first select the algorithm against which to play: enter "1" to play against Minimax, or "2" to play against the Evolutionary Algorithm.
If you choose to play against Minimax, you will be asked to enter the level of difficulty you want to play against, a number between 1 and 5. Once you've entered the level, a PyGame window will open and you can start playing the game.



Connect Four: AI Battle - Minimax vs Evolutionary Algorithm
This Python script creates a version of Connect Four in which two artificial intelligence (AI) players battle against each other: one uses the minimax algorithm with alpha-beta pruning, while the other uses an evolutionary algorithm (EA).
Usage
To run this script, simply execute it in your Python environment. A Pygame window will open and the game will start. The game will automatically play rounds of Connect Four until you close the window.
During each round, the minimax AI and the evolutionary algorithm AI will take turns placing their pieces on the board, with the goal of getting four of their pieces in a row (horizontally, vertically, or diagonally) before the other player does.
Components
This script contains the following main components:
•	Individual class: Represents an individual solution (i.e., a game board state) in the evolutionary algorithm's population.
•	create_board(): Creates an empty game board.
•	drop_piece(): Drops a piece onto the game board.
•	winning_move(): Checks if a player has won the game.
•	create_population(): Creates the initial population for the evolutionary algorithm.
•	selection(): Selects the fittest individuals in the population for reproduction.
•	crossover(): Generates a new individual by crossing over two parents.
•	mutate(): Mutates an individual with a chance of MUTATION_RATE.
•	create_new_generation(): Creates a new generation of individuals.
•	evolutionary_algorithm(): Executes the evolutionary algorithm, ultimately selecting the best move for the EA player.
•	minimax(): Executes the minimax algorithm with alpha-beta pruning, ultimately selecting the best move for the minimax player.
•	draw_board(): Draws the game board using Pygame.
•	pick_best_move(): Scores all possible moves and selects the best one.
•	location_valid_gets(): Returns all valid moves in the current game state.
•	is_terminal_node(), score_position(), evaluate_window(): Functions used to help the minimax algorithm evaluate the game board.
Output
The output of this script is a visualization of the game board as the AI players take their turns. After each game, it will print out the current score and winning player information. The game will continue running until the Pygame window is closed.
The AI players' winning data is stored in a pickle file named "winning_data.pickle". This includes the number of wins for each AI player, as well as the number of draws.
Customization
You can modify the AI players' behavior by adjusting the following parameters:
•	POPULATION_SIZE: The size of the evolutionary algorithm's population.
•	GENERATIONS: The number of generations that the evolutionary algorithm will run for.
•	MUTATION_RATE: The chance that an individual will be mutated in the evolutionary algorithm.
•	depth: The depth to which the minimax algorithm will search. This parameter can be adjusted by the user when running the script, with higher values corresponding to more difficult AI opponents.

