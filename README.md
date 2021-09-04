# PatzerChess

![image](https://user-images.githubusercontent.com/73597280/131067264-f9df7262-f395-4422-800f-e229516ad1b5.png)

PatzerChess is an engine that is tries to best simulate the play of a human, while somewhat avoiding the oversights that humans have.

The program will try to simulate human play through either changing and modifying the evaluation function to better represent the human move, or by relying on a ML for both its evaluation functions and monte-carlo search function. Depending on how strong the engine should be, seperate endgame, opening, and middlegame bots might be advantageous to try to cover up the oversights that a middlegame bot might have when looking at the endgame.

Currently, PatzerChess is no different from any other chess engine, using traditional search and evaluation functions as a proof of concept of our board representation, but eventually we would start to implement the part that starts to play like a human. 

## Navigating the code

All code files will be under /src.

Board.py - contains the board representation and move generation function
Eval.py - the traditional evaluation function without any neural networks (empty)
Parsefen.py - parsing a fen string in order to convert it into a board representation

## Sources and references

- [Logo](https://www.frankerfacez.com/emoticon/471255-PeepoChess)
- [LC0, NN reference](https://lczero.org/)
- [PUCT Monte-Carlo Search](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.172.9450&rep=rep1&type=pdf)
- [Monte Carlo Search](https://hal.archives-ouvertes.fr/hal-00747575v4/document)
- [AlphaZero Paper](https://arxiv.org/pdf/1712.01815.pdf)
- [ChessProgramming Wiki](https://www.chessprogramming.org/Main_Page)
- [Sunfish by Thomasalhe](https://github.com/thomasahle/sunfish)
- [Coding Adventure - Chess AI by Sebastian Lague](https://www.youtube.com/watch?v=U4ogK0MIzqk&t=128s)
- [Chess Alpha Zero - Electric Boogaloo](https://github.com/Zeta36/chess-alpha-zero)
- [GarbochessJS, using as a way to reference SF](https://github.com/glinscott/Garbochess-JS)
- [Programming an Advanced Chess Engine - Logic Crazy](https://www.youtube.com/playlist?list=PLQV5mozTHmacMeRzJCW_8K3qw2miYqd0c)
