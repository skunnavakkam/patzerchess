/// Look up table for population count
/// Only applies to 8 bit integers
/// Used in popcnt_table for 64 bit ints
const POPCNT8: [u8; 256] = [
    0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    1, 2, 2, 3, 2, 3, 3, 4, 2, 3, 3, 4, 3, 4, 4, 5, 2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    2, 3, 3, 4, 3, 4, 4, 5, 3, 4, 4, 5, 4, 5, 5, 6, 3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7,
    3, 4, 4, 5, 4, 5, 5, 6, 4, 5, 5, 6, 5, 6, 6, 7, 4, 5, 5, 6, 5, 6, 6, 7, 5, 6, 6, 7, 6, 7, 7, 8,
];

/// popcnt implementation
/// Can also use .count_ones() thought I think this might be more efficient
#[inline]
fn popcnt_table(x: u64) -> u8 {
    let x = x as usize;
    if x == 0 {
        return 0;
    }
    if x & (x.wrapping_sub(1)) == 0 {
        return 1;
    }

    POPCNT8[x >> 56]
        + POPCNT8[(x >> 48) & 0xFF]
        + POPCNT8[(x >> 40) & 0xFF]
        + POPCNT8[(x >> 32) & 0xFF]
        + POPCNT8[(x >> 24) & 0xFF]
        + POPCNT8[(x >> 16) & 0xFF]
        + POPCNT8[(x >> 8) & 0xFF]
        + POPCNT8[x & 0xFF]
}

pub fn material_eval(position: Position) -> i32 {
    let piece_values: [i32; 12] = [
        100, 295, 350, 480, 920, 30000, -100, -295, -350, -480, -920, -30000,
    ];
    let mut eval = 0;
    for (piece, board) in position.boards.iter().enumerate() {
        println!("{:?}", popcnt_table(*board));
        eval += (popcnt_table(*board) as i32) * piece_values[piece]
    }

    return eval;
}
