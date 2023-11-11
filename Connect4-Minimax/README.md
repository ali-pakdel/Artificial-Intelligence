# Connect4 AI with Minimax Algorithm

This project designed to challenge your skills against a formidable AI opponent in the classic game of Connect 4. This implementation incorporates the Minimax algorithm, infusing strategic intelligence into the gameplay.

## Objective

The aim of this project is to anticipate the opponent's moves using the Minimax algorithm, striving for victory in the Connect 4 game.

## Development Phases

This project unfolds in two crucial phases, each showcasing a distinct Minimax strategy:

### Phase 1: Minimax with Pruning
In the initial phase, the AI employs the Minimax algorithm with pruning techniques. Pruning optimizes the search space, enhancing efficiency without compromising accuracy.

### Phase 2: Minimax without Pruning
The second phase focuses on Minimax without pruning, allowing for an exhaustive exploration of all possible moves, providing a deeper analysis of the game state.

## Game Description

In Connect 4, players take turns choosing a column to drop their pieces. Pieces fall down the chosen column until they either land on another piece or reach the bottom row. The Minimax algorithm precisely predicts the opponent's moves. The depth parameter controls the algorithm's accuracy, with a higher depth improving precision but also increasing time complexity and victory chances.

## Heuristic Function

A thoughtfully designed heuristic function evaluates optimal moves, prioritizing positions leading to winning states, such as placing a piece next to an existing row of three marbles. Additionally, the function focuses on blocking the opponent's potential winning moves. By assigning values to each board cell, this optimized and consistent heuristic ensures strategic decision-making.

## Verification and Accuracy

To ensure algorithm accuracy, various instances of the game table were evaluated. These assessments validate the AI's performance, ensuring efficiency and accuracy in different gameplay scenarios.

## Usage

To experience Connect4 AI, instantiate the `ConnectSin` class, set the desired maximum depth for the Minimax algorithm, and choose whether to enable pruning for reduced time complexity. The AI can be played against a human opponent, offering a challenging and engaging gameplay experience.
