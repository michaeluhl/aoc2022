use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;


static BEATS: &[char] = &['Z', 'X', 'Y'];


fn score(o: char, m: char) -> i32 {
    let ord: usize = (m as usize - 88).into();
    let score: i32 = if o == BEATS[ord] {
        6
    } else if o == m {
        3
    } else {
        0
    } + ord as i32 + 1;
    return score;
}


fn ldw(o: char, m: char) -> i32 {
    let ord: usize = (o as usize - 88).into();
    let m_ = match m {
        'Y' => o,
        'X' => BEATS[ord],
        'Z' => BEATS[(ord + 2) % 3],
        _ => panic!("Should only be X, Y, or Z")
    };
    return score(o, m_);
}


fn main() -> io::Result<()> {
    let f = File::open("input.txt")?;
    let reader = BufReader::new(f);

    let mut totals_v1: i32 = 0;
    let mut totals_v2: i32 = 0;
    
    for line_ in reader.lines() {
        let line: String = line_?;
        let mut chars: Vec<char> = line.trim().chars().collect();
        chars[0] = match chars[0] {
            'A' => 'X',
            'B' => 'Y',
            'C' => 'Z',
            _ => panic!()
        };
        totals_v1 += score(chars[0], chars[2]);
        totals_v2 += ldw(chars[0], chars[2]);

    }

    println!("{}", totals_v1);
    println!("{}", totals_v2);

    return Ok(());
}