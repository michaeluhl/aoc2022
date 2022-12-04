use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;


fn main() -> io::Result<()> {
    let f: File = File::open("input.txt")?;
    let reader: BufReader<File> = BufReader::new(f);

    let mut n_contains: i32 = 0;
    let mut n_overlaps: i32 = 0;

    for line_ in reader.lines() {
        let line: String = line_?;
        let (r1, r2) = line.split_once(",").unwrap();
        let r1r: Vec<i32> = r1.split("-").map(|v| v.parse::<i32>().unwrap()).collect();
        let r2r: Vec<i32> = r2.split("-").map(|v| v.parse::<i32>().unwrap()).collect();
        if (r2r[0] >= r1r[0]) && (r2r[1] <= r1r[1]) {
            n_contains += 1;
        } else if (r1r[0] >= r2r[0]) && (r1r[1] <= r2r[1]) {
            n_contains += 1;
        }
        if (r2r[1] >= r1r[0]) && (r2r[0] <= r1r[1]) {
            n_overlaps += 1;
        } else if (r1r[1] >= r2r[0]) && (r1r[0] <= r2r[1]) {
            n_overlaps += 1;
        }
    }

    println!("{}", n_contains);
    println!("{}", n_overlaps);

    return Ok(());
}