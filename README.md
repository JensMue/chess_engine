# Building a chess engine in Python

This is a project by Jens Mueller.

The goal of this project was to build a simple chess engine in Python using a negamax algorithm.
The engine was additionally improved with several techniques including alpha-beta pruning, move-ordering, opening book, and endgame tablebases.

Please refer to ```./doc/chess_engine_presentation.pdf``` for an overview of the project.

If you have any problems, questions, or suggestions, please contact me at jens.mueller@studbocconi.it


## Quickstart

You can play the program by typing ```python chess_engine``` in the terminal or in an editor like Visual Studio Code.

Alternatively, you can manually run ```__main__py```.



## Repository structure

```bash
chess_engine
│   .gitignore
│   README.txt
│   requirements.txt
│   __main__.py
│
├───doc
│       chess_engine_presentation.pdf
│
├───res
│   ├───polyglot_opening_book/
│   │       SOURCE.txt
│   │
│   └───syzygy_endgame_tablebases/
│           SOURCES.txt
│
├───src
│   └───chess_engine
│           engine_negamax.py
│           engine_simple.py
│           engine_versions.py
│           evaluation.py
│           game_formats.py
│           player_human.py
│           setup.py
│           utils.py
│           __init__.py
│
└───test
        tests.ipynb
```

## Data

Optionally, an opening book and endgame tablebases can be downloaded from the sources indicated in ```./res/``` to improve the engine.

## Sources

- https://www.chessprogramming.org/Alpha-Beta
- https://www.chessprogramming.org/Endgame_Tablebases
- https://www.chessprogramming.org/Killer_Heuristic
- https://www.chessprogramming.org/Minimax
- https://www.chessprogramming.org/Move_Ordering
- https://www.chessprogramming.org/Negamax
- https://www.chessprogramming.org/Opening_Book
- https://www.chessprogramming.org/Quiescence_Search
- https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
- https://www.slideshare.net/myemon/aiminimax-algorithm-and-alpha-beta-reduction
- https://www.slideshare.net/RohitVaidya3/how-i-taught-a-computer-to-play-chess
- https://www.youtube.com/watch?v=l-hh51ncgDI&list=WL&index=7&t=0s
- https://byanofsky.com/2017/07/06/building-a-simple-chess-ai/
- https://en.wikipedia.org/Minimax
- https://python-chess.readthedocs.io/en/latest/index.html
