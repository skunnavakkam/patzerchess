mod board;
mod eval;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let mut board = board::Position {
        mailbox: [13; 64],
        boards: [0; 12],
        black_board: 0,
        white_board: 0,
        occupied: 0,
        castling: [false; 4],
        ep: 0,
        fm: 0,
        hm: 0,
        is_white: false,
    };

    // its ur fault if you fuck up by using an incorrect string
    board.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");

    let wp_moves = board.wp_gen(board.boards[0]);

    println!("{}", board.print_pretty(board.boards[3]));
}
