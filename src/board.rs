#[derive(Debug)]
pub struct Position {
    pub mailbox: [u8; 64],
    pub boards: [u64; 12],
    pub black_board: u64,
    pub white_board: u64,
    pub occupied: u64,
    pub castling: [bool; 4],
    pub ep: u8,
    pub fm: u8,
    pub hm: u8,
    pub is_white: bool,
}

impl Position {
    /// Helper Function take from chessprogramming wiki
    /// https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating
    fn flip_vertical(&self, x: u64) -> u64 {
        return (x << 56)
            | ((x << 40) & 0x00ff000000000000)
            | ((x << 24) & 0x0000ff0000000000)
            | ((x << 8) & 0x000000ff00000000)
            | ((x >> 8) & 0x00000000ff000000)
            | ((x >> 24) & 0x0000000000ff0000)
            | ((x >> 40) & 0x000000000000ff00)
            | (x >> 56);
    }

    /// Helper function taken from chessprogramming wiki
    /// https://www.chessprogramming.org/Flipping_Mirroring_and_Rotating
    fn mirror_horizontal(&self, mut x: u64) -> u64 {
        let k1 = 0x5555555555555555;
        let k2 = 0x3333333333333333;
        let k4 = 0x0f0f0f0f0f0f0f0f;
        x = ((x >> 1) & k1) + 2 * (x & k1);
        x = ((x >> 2) & k2) + 4 * (x & k2);
        x = ((x >> 4) & k4) + 16 * (x & k4);
        return x;
    }

    pub fn print_pretty(&self, bitboard: u64) -> String {
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

    pub fn parse_fen(&mut self, input_fen: &str) {
        let fen = input_fen.to_string();
        let elements = fen.split(' ').collect::<Vec<&str>>();
        let pieces = elements[0].replace("/", "");

        let mut square = 0u16;
        for piece in pieces.chars() {
            if piece.is_digit(10) {
                square += piece as u16 - '0' as u16;
                continue;
            }

            if piece.to_string() > "A".to_string() {
                self.white_board |= 1 << square
            } else {
                self.black_board |= 1 << square
            }

            if piece == 'P' {
                self.boards[0] ^= 1 << square;
            } else if piece == 'N' {
                self.boards[1] ^= 1 << square;
            } else if piece == 'B' {
                self.boards[2] ^= 1 << square;
            } else if piece == 'R' {
                self.boards[3] ^= 1 << square;
            } else if piece == 'Q' {
                self.boards[4] ^= 1 << square;
            } else if piece == 'K' {
                self.boards[5] ^= 1 << square;
            } else if piece == 'p' {
                self.boards[6] ^= 1 << square;
            } else if piece == 'n' {
                self.boards[7] ^= 1 << square;
            } else if piece == 'b' {
                self.boards[8] ^= 1 << square;
            } else if piece == 'r' {
                self.boards[9] ^= 1 << square;
            } else if piece == 'q' {
                self.boards[10] ^= 1 << square;
            } else if piece == 'k' {
                self.boards[11] ^= 1 << square;
            }

            square += 1
        }

        self.occupied = self.white_board | self.black_board;

        let color = elements[1];
        let ep = elements[3];
        self.fm = elements[5].parse::<u8>().unwrap();
        self.hm = elements[4].parse::<u8>().unwrap();

        self.is_white = color == "w";

        if ep != "-" {
            self.ep = ep.parse::<u8>().unwrap();
        } else {
            self.ep = 255;
        }
    }

    pub fn wp_gen(&self, input: u64) -> u64 {
        if input != 0 {
            let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
            let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
            let rank3 = 0b0000000000000000111111110000000000000000000000000000000000000000u64;

            let single_move = (input >> 8) & !self.occupied;
            let pawn_attacks = ((input & not_h) >> 7) | ((input & not_a) >> 9);
            let double_move = ((single_move & rank3) >> 8) & !self.occupied;
            let pawn_captures = pawn_attacks & self.black_board;

            return double_move | single_move | pawn_captures;
        }
        return 0u64;
    }

    pub fn wn_gen(&self, input: u64) -> u64 {
        if input != 0 {
            // masks
            let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
            let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
            let not_ab = 0b1111110011111100111111001111110011111100111111001111110011111100u64;
            let not_gh = 0b0011111100111111001111110011111100111111001111110011111100111111u64;

            // variables named as
            // 2 move direction 1 move direction
            // moving two squares n and 1 square e would be ne
            let ne_moves = (input >> 15) & not_a & !self.white_board;
            let nw_moves = (input >> 17) & not_h & !self.white_board;
            let en_moves = (input >> 6) & not_ab & !self.white_board;
            let es_moves = (input << 10) & not_ab & !self.white_board;

            let se_moves = (input << 17) & not_a & !self.white_board;
            let sw_moves = (input << 15) & not_h & !self.white_board;

            let wn_moves = (input >> 10) & not_gh & !self.white_board;
            let ws_moves = (input << 6) & not_gh & !self.white_board;

            return ne_moves
                | nw_moves
                | en_moves
                | es_moves
                | se_moves
                | sw_moves
                | wn_moves
                | ws_moves;
        }

        return 0;
    }

    pub fn wk_gen(&self, input: u64) -> u64 {
        if input != 0 {
            let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
            let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;

            let e_move = (input << 1) & not_a;
            let w_move = (input >> 1) & not_h;

            let horizontal = e_move | input | w_move;
            let king_moves: u64 = ((horizontal) << 8) | e_move | w_move | (horizontal >> 8);

            return king_moves;
        }
        return 0;
    }

    pub fn wb_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b0000000011111111111111111111111111111111111111111111111111111111u64;

        let mut moves = 0;
        if input != 0 {
            let mut wb_ne = input;
            let mut wb_nw = input;
            let mut wb_se = input;
            let mut wb_sw = input;

            for _ in 1..8 {
                // seperate iterations for each direction
                wb_ne = ((wb_ne & not_h) >> 7) & !self.white_board;
                wb_nw = ((wb_nw & not_a) >> 9) & !self.white_board;
                wb_se = ((wb_se & not_1 & not_h) << 9) & !self.white_board;
                wb_sw = ((wb_sw & not_1 & not_a) << 7) & !self.white_board;

                moves = moves | wb_ne | wb_nw | wb_se | wb_sw;

                wb_ne &= !self.occupied;
                wb_nw &= !self.occupied;
                wb_se &= !self.occupied;
                wb_sw &= !self.occupied;

                if (wb_ne + wb_nw + wb_se + wb_sw) == 0 {
                    break;
                }
            }
        }
        return moves;
    }

    pub fn wr_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b0000000011111111111111111111111111111111111111111111111111111111u64;

        let mut moves = 0;
        if input != 0 {
            let mut wr_west = input;
            let mut wr_east = input;
            let mut wr_north = input;
            let mut wr_south = input;

            for _ in 1..8 {
                // seperate iterations for each direction
                wr_west = ((wr_west & not_a) >> 1) & !self.white_board;
                wr_east = ((wr_east & not_h) << 1) & !self.white_board;
                wr_north = (wr_north >> 8) & !self.white_board;
                wr_south = ((wr_south & not_1) << 8) & !self.white_board;

                moves = moves | wr_west | wr_east | wr_north | wr_south;

                wr_south &= !self.black_board;
                wr_north &= !self.black_board;
                wr_east &= !self.black_board;
                wr_west &= !self.black_board;

                if (wr_north + wr_south + wr_east + wr_north) == 0 {
                    break;
                }
            }
        }

        return moves;
    }

    pub fn wq_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b0000000011111111111111111111111111111111111111111111111111111111u64;

        let mut moves = 0;
        if input != 0 {
            let mut wq_west = input;
            let mut wq_east = input;
            let mut wq_north = input;
            let mut wq_south = input;
            let mut wq_ne = input;
            let mut wq_nw = input;
            let mut wq_se = input;
            let mut wq_sw = input;

            for _ in 1..8 {
                // seperate iterations for each direction
                wq_west = ((wq_west & not_a) >> 1) & !self.white_board;
                wq_east = ((wq_east & not_h) << 1) & !self.white_board;
                wq_north = (wq_north >> 8) & !self.white_board;
                wq_south = ((wq_south & not_1) << 8) & !self.white_board;
                wq_ne = ((wq_ne & not_h) >> 7) & !self.white_board;
                wq_nw = ((wq_nw & not_a) >> 9) & !self.white_board;
                wq_se = ((wq_se & not_1 & not_h) << 9) & !self.white_board;
                wq_sw = ((wq_sw & not_1 & not_a) << 7) & !self.white_board;

                moves =
                    moves | wq_west | wq_east | wq_north | wq_south | wq_ne | wq_nw | wq_se | wq_sw;

                wq_south &= !self.occupied;
                wq_north &= !self.occupied;
                wq_east &= !self.occupied;
                wq_west &= !self.occupied;
                wq_ne &= !self.occupied;
                wq_nw &= !self.occupied;
                wq_se &= !self.occupied;
                wq_sw &= !self.occupied;

                if (wq_north + wq_south + wq_east + wq_north + wq_ne + wq_nw + wq_se + wq_sw) == 0 {
                    break;
                }
            }
        }
        return moves;
    }

    pub fn bp_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let rank6 = 0b0000000000000000000000000000000000000000111111110000000000000000u64;

        if input != 0 {
            let single_move = (input << 8) & !self.occupied;
            let pawn_attacks = ((input & not_h) << 7) | ((input & not_a) << 9);
            let double_move = ((single_move & rank6) << 8) & !self.occupied;
            let pawn_captures = pawn_attacks & self.white_board;

            return pawn_captures | double_move | single_move;
        }

        return 0;
    }

    pub fn bn_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_ab = 0b1111110011111100111111001111110011111100111111001111110011111100u64;
        let not_gh = 0b0011111100111111001111110011111100111111001111110011111100111111u64;

        if input != 0 {
            // variables named as
            // 2 move direction 1 move direction
            // moving two squares n and 1 square e would be ne
            let ne_moves = (input >> 15) & not_a & !self.white_board;
            let nw_moves = (input >> 17) & not_h & !self.white_board;
            let en_moves = (input >> 6) & not_ab & !self.white_board;
            let es_moves = (input << 10) & not_ab & !self.white_board;

            let se_moves = (input << 17) & not_a & !self.white_board;
            let sw_moves = (input << 15) & not_h & !self.white_board;

            let wn_moves = (input >> 10) & not_gh & !self.white_board;
            let ws_moves = (input << 6) & not_gh & !self.white_board;

            return ne_moves
                | nw_moves
                | en_moves
                | es_moves
                | se_moves
                | sw_moves
                | wn_moves
                | ws_moves;
        }
        return 0;
    }

    pub fn bk_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;

        if input != 0 {
            let e_move = (input << 1) & not_a;
            let w_move = (input >> 1) & not_h;

            let horizontal = e_move | input | w_move;
            let king_moves: u64 = ((horizontal) << 8) | e_move | w_move | (horizontal >> 8);
            return king_moves;
        }

        return 0;
    }

    pub fn bb_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b0000000011111111111111111111111111111111111111111111111111111111u64;

        let mut moves = 0;
        if input != 0 {
            let mut bb_ne = input;
            let mut bb_nw = input;
            let mut bb_se = input;
            let mut bb_sw = input;

            for _ in 1..8 {
                // seperate iterations for each direction
                bb_ne = ((bb_ne & not_h) >> 7) & !self.black_board;
                bb_nw = ((bb_nw & not_a) >> 9) & !self.black_board;
                bb_se = ((bb_se & not_1 & not_h) << 9) & !self.black_board;
                bb_sw = ((bb_sw & not_1 & not_a) << 7) & !self.black_board;

                moves = moves | bb_ne | bb_nw | bb_se | bb_sw;

                bb_ne &= !self.occupied;
                bb_nw &= !self.occupied;
                bb_se &= !self.occupied;
                bb_sw &= !self.occupied;

                if (bb_ne + bb_nw + bb_se + bb_sw) == 0 {
                    break;
                }
            }
        }
        return moves;
    }

    pub fn br_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b0000000011111111111111111111111111111111111111111111111111111111u64;

        let mut moves = 0;
        if input != 0 {
            let mut br_west = input;
            let mut br_east = input;
            let mut br_north = input;
            let mut br_south = input;

            for _ in 1..8 {
                // seperate iterations for each direction
                br_west = ((br_west & not_a) >> 1) & !self.black_board;
                br_east = ((br_east & not_h) << 1) & !self.black_board;
                br_north = (br_north >> 8) & !self.black_board;
                br_south = ((br_south & not_1) << 8) & !self.black_board;

                moves = moves | br_west | br_east | br_north | br_south;

                br_south &= !self.occupied;
                br_north &= !self.occupied;
                br_east &= !self.occupied;
                br_west &= !self.occupied;

                if (br_north + br_south + br_east + br_north) == 0 {
                    break;
                }
            }
        }
        return moves;
    }

    pub fn bq_gen(&self, input: u64) -> u64 {
        let not_a = 0b1111111011111110111111101111111011111110111111101111111011111110u64;
        let not_h = 0b0111111101111111011111110111111101111111011111110111111101111111u64;
        let not_1 = 0b0000000011111111111111111111111111111111111111111111111111111111u64;

        let mut moves = 0;
        if input != 0 {
            let mut bq_west = input;
            let mut bq_east = input;
            let mut bq_north = input;
            let mut bq_south = input;
            let mut bq_ne = input;
            let mut bq_nw = input;
            let mut bq_se = input;
            let mut bq_sw = input;

            for _ in 1..8 {
                // seperate iterations for each direction
                bq_west = ((bq_west & not_a) >> 1) & !self.black_board;
                bq_east = ((bq_east & not_h) << 1) & !self.black_board;
                bq_north = (bq_north >> 8) & !self.black_board;
                bq_south = ((bq_south & not_1) << 8) & !self.black_board;
                bq_ne = ((bq_ne & not_h) >> 7) & !self.black_board;
                bq_nw = ((bq_nw & not_a) >> 9) & !self.black_board;
                bq_se = ((bq_se & not_1 & not_h) << 9) & !self.black_board;
                bq_sw = ((bq_sw & not_1 & not_a) << 7) & !self.black_board;

                moves =
                    moves | bq_west | bq_east | bq_north | bq_south | bq_ne | bq_nw | bq_se | bq_sw;

                bq_south &= !self.occupied;
                bq_north &= !self.occupied;
                bq_east &= !self.occupied;
                bq_west &= !self.occupied;
                bq_ne &= !self.occupied;
                bq_nw &= !self.occupied;
                bq_se &= !self.occupied;
                bq_sw &= !self.occupied;

                if (bq_north + bq_south + bq_east + bq_north + bq_ne + bq_nw + bq_se + bq_sw) == 0 {
                    break;
                }
            }
        }
        return moves;
    }
}
