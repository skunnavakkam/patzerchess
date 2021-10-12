mod board;
mod eval;

fn main() {
    let mut board = board::Position {
        mailbox: [0; 64],
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

    println!("{:#b}", board.boards[0]);
}
