# Building a simple chess engine

This is a project by Jens Mueller.
It was conducted as part of the course Computer Science (Algorithms) at Bocconi University.
The project was presented on June 12, 2020.

Please refer to 'chess_engine_presentation.pdf' for an overview of the project.

The goal of this project was to build a simple chess engine using a minimax algorithm.
This engine was additionally improved with several techniques including alpha-beta pruning,
move-ordering, Quiescence search, opening book, and endgame tablebase.

If you have any problems, questions, or suggestions, please contact me at jens.mueller@studbocconi.it


## Repository structure

```
msc_thesis/
│   README.md
│   chess_engine_presentation.pdf
│
│   games.py		---functions for playing chess
│   players.py		---classes for the available players and engines
│   player_history.py	---old engine versions (for documentation only)
│   analysis.ipynb	---some analyses used in the final presentation
│   play.py		---play chess against the engine
│   utils.py		---helper functions used throughout the project
│
└───polyglot/		---polyglot opening book
└───syzygy/		---syzygy endgame tablebase
```

The project requires the library python-chess.


## Recommended usage

You can play against the engine  by simply running the file play.py in an editor like Visual Studio Code.
The file can also be executed in the terminal, but the unicode board might not get represented correctly in that case.
The folder structure should be left as is.
