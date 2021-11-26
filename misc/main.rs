use chess::*;

fn main() {
    let init_position_2 =
        Board::from_str("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");

    let movegen = MoveGen::new_legal(&init_position_2);

    assert_eq!(movegen.len(), 20);
}
