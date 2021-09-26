#[derive(Debug, Default)]
struct Position {
    wp: u64,
    wn: u64,
    wb: u64,
    wr: u64,
    wq: u64,
    wk: u64,
    bp: u64,
    bn: u64,
    bb: u64,
    br: u64,
    bq: u64,
    bk: u64,
    black_board: u64,
    white_board: u64,
    castling: [bool; 4],
    ep: u8,
    fm: u8,
    hm: u8,
    is_white: bool,
}

impl Position {
    // don't have to worry about efficieny in this part since
    // it probably only will run once
    fn parse_fen(&mut self, input_fen: &str) {
        let fen = input_fen.to_string();
        let elements = fen.split(' ').collect::<Vec<&str>>();
        let piece_list = elements[0].replace("/", "");
        println!("{:?}", piece_list);

        let ep = elements[3];
        let fm = elements[5];
        let hm = elements[4];
        let mut piece_string: String = "".to_string();

        if ep != "-" {
            self.ep = ep.parse::<u8>().unwrap();
        } else {
            self.ep = 255;
        }
        // doing this not for efficieny but just to make it easier to code
        for piece in piece_list.chars() {
            if piece.is_digit(10) {
                piece_string += &' '.to_string().repeat((piece as usize) - 0x30);
            } else {
                piece_string += &piece.to_string();
            }
        }

        for (square, piece) in piece_string.chars().enumerate() {
            if piece == 'P' {
                self.wp ^= 1 << square;
            } else if piece == 'N' {
                self.wn ^= 1 << square;
            } else if piece == 'B' {
                self.wb ^= 1 << square;
            } else if piece == 'R' {
                self.wr ^= 1 << square;
            } else if piece == 'Q' {
                self.wq ^= 1 << square;
            } else if piece == 'K' {
                self.wk ^= 1 << square;
            }

            if piece == 'p' {
                self.bp ^= 1 << square;
            } else if piece == 'n' {
                self.bn ^= 1 << square;
            } else if piece == 'b' {
                self.bb ^= 1 << square;
            } else if piece == 'r' {
                self.br ^= 1 << square;
            } else if piece == 'q' {
                self.bq ^= 1 << square;
            } else if piece == 'k' {
                self.bk ^= 1 << square;
            }

            if (piece >= 'A') & (piece != ' ') {
                self.white_board ^= 1 << square;
            } else if piece != ' ' {
                self.black_board ^= 1 << square;
            }
        }
    }

    // don't have to worry about efficieny here as well
    // try it if you hate yourself
    fn print_pretty(&self, bitboard: u64) -> String {
        let mut as_string = format!("{:#b}", bitboard).to_string();
        as_string.remove(0);
        as_string.remove(0);

        let mut string_to_print = "\n".to_string();

        for (square, bit) in as_string.chars().rev().enumerate() {
            string_to_print.push_str(&bit.to_string());
            string_to_print.push_str(" ");
            if square % 8 == 7 {
                string_to_print.push_str("\n");
            }
        }

        return string_to_print;
    }

    fn _gen_out_of_check(&self) {
        //general masks
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b1111111100000000000000000000000000000000000000000000000000000000u64;

        // pawn masks
        let rank3 = 0b0000000000000000111111110000000000000000000000000000000000000000u64;
        let rank6 = 0b0000000000000000000000000000000000000000111111110000000000000000u64;

        //knight masks
        let not_ab = 0b1111110011111100111111001111110011111100111111001111110011111100u64;
        let not_gh = 0b0011111100111111001111110011111100111111001111110011111100111111u64;

        let wb_board = self.black_board | self.white_board;
        let wb_board_flip = !wb_board;
        let white_board_flip = !self.white_board;
        let black_board_flip = !self.black_board;

        if self.wp != 0 {
            let single_move = (self.wp >> 8) & wb_board_flip;
            let pawn_attacks = ((self.wp & not_h) >> 7) | ((self.wp & not_a) >> 9);
            let double_move = ((single_move & rank3) >> 8) & wb_board_flip;
            let pawn_captures = pawn_attacks & self.black_board;
        }

        if self.wn != 0 {
            // variables named as
            // 2 move direction 1 move direction
            // moving two squares N and 1 square E would be NE
            let ne_moves = (self.wn >> 15) & not_a & white_board_flip;
            let nw_moves = (self.wn >> 17) & not_h & white_board_flip;
            let en_moves = (self.wn >> 6) & not_ab & white_board_flip;
            let es_moves = (self.wn << 10) & not_ab & white_board_flip;

            let se_moves = (self.wn << 17) & not_a & white_board_flip;
            let sw_moves = (self.wn << 15) & not_h & white_board_flip;

            let wn_moves = (self.wn >> 10) & not_gh & white_board_flip;
            let ws_moves = (self.wn << 6) & not_gh & white_board_flip;

            let knight_moves = ne_moves
                | nw_moves
                | en_moves
                | es_moves
                | se_moves
                | sw_moves
                | wn_moves
                | ws_moves;
        }

        if self.wk != 0 {
            let e_move = (self.wk << 1) & not_a;
            let w_move = (self.wk >> 1) & not_h;

            let horizontal = e_move | self.wk | w_move;
            let king_moves: u64 = ((horizontal) << 8) | e_move | w_move | (horizontal >> 8);
        }

        // --------------------------------------Sliding Pieces--------------------------------------

        if self.wr != 0 {
            let mut moves = 0;
            let mut wr_west = self.wr;
            let mut wr_east = self.wr;
            let mut wr_north = self.wr;
            let mut wr_south = self.wr;

            for _ in 1..8 {
                // seperate iterations for each direction
                wr_west = ((wr_west & not_h) >> 1) & white_board_flip;
                wr_east = ((wr_east & not_a) << 1) & white_board_flip;
                wr_north = (wr_north >> 8) & white_board_flip;
                wr_south = ((wr_south & not_1) << 8) & white_board_flip;

                moves = moves | wr_west | wr_east | wr_north | wr_south;

                wr_south &= black_board_flip;
                wr_north &= black_board_flip;
                wr_east &= black_board_flip;
                wr_west &= black_board_flip;

                if (wr_north + wr_south + wr_east + wr_north) == 0 {
                    break;
                }
            }

            println!("{}", moves)
        }
    }
}

fn main() {
    let mut board = Position::default();

    // its ur fault if you fuck up by using an incorrect string
    board.parse_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    board._gen_out_of_check();
}
