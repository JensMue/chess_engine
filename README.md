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

## Sources

https://python-chess.readthedocs.io/en/latest/index.html
https://www.chessprogramming.org/Minimax
https://www.chessprogramming.org/Negamax
https://www.chessprogramming.org/Alpha-Beta
https://www.chessprogramming.org/Move_Ordering
https://www.chessprogramming.org/Killer_Heuristic
https://www.chessprogramming.org/Opening_Book
https://www.chessprogramming.org/Endgame_Tablebases
https://www.chessprogramming.org/Quiescence_Search
https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
https://byanofsky.com/2017/07/06/building-a-simple-chess-ai/
https://www.youtube.com/watch?v=l-hh51ncgDI&list=WL&index=7&t=0s
https://www.slideshare.net/RohitVaidya3/how-i-taught-a-computer-to-play-chess
https://www.slideshare.net/myemon/aiminimax-algorithm-and-alpha-beta-reduction
https://en.wikipedia.org/Minimax
