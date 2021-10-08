mod board;
mod perftests;

fn main() {
    let mut board = board::Position::default();

    // its ur fault if you fuck up by using an incorrect string
    board.parse_fen("8/8/8/2B5/8/8/8/8 w - - 0 1");

    println!(
        "{:#?}",
        perftests::time_out_of_check("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    )
}
