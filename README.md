# Chess Trainer

An interactive tool to practice finding the best move in any given chess position.

GIF...

## About

This tool is an interactive chess trainer that lets you practice your chess understanding by loading random positions on an interactive chess board to solve. After you make your move, the software displays the loss (difference between the best engine move and your own move) and the engine evaluation of the position. It also features a live engine showing the 5 best moves for you to analyze each position in more detail. You can use the left-arrow and right-arrow keys to go back and forth between moves. To go to the next position, press the `Next` button. Positions can be reset to their original state by using the `Reset` button.

## Usage

Clone this repository.

```
git clone https://github.com/marcohenning/chess.git
```

Download the open source  chess engine [Stockfish](https://stockfishchess.org/) and move the `stockfish` folder into the `src` folder of this project.

The program can now be started by running `main.py`.

## Data

The positions have all been taken from the lichess.org open database, which features billions of chess games played on the lichess platform. I extracted random positions from a portion of this database and saved them in the `positions` directory for quick access.

## License

This software is licensed under the [MIT license](https://github.com/marcohenning/chess/blob/master/LICENSE).