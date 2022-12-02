use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;


fn main() -> io::Result<()> {
    let f = File::open("input.txt")?;
    let reader = BufReader::new(f);

    let mut totals: Vec<i32> = Vec::new();
    let mut accum: Vec<i32> = Vec::new();

    for line in reader.lines() {
        let linev: String = line?;
        let trimmed: &str = linev.trim();
        if trimmed == "" {
            totals.push(accum.iter().sum());
            accum.clear();
        } else {
            accum.push(trimmed.parse::<i32>().expect("Expected integer"));
        }
    }
    totals.push(accum.iter().sum());

    totals.sort();
    totals.reverse();
    println!("{}", totals[0]);
    println!("{}", totals[0..3].iter().sum::<i32>());
    return Ok(());
}