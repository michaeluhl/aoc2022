use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::collections::HashSet;


fn main() -> io::Result<()> {
    let f:File = File::open("input.txt")?;
    let reader: BufReader<File> = BufReader::new(f);

    for line_ in reader.lines() {
        let line = line_?;
        let ss = &line;
        let mut hset:HashSet<char> = HashSet::new();
        for i in 0..ss.len() - 4 {
            hset.extend(ss[i..i+4].chars());
            if hset.len() == 4 {
                println!("{}", i + 4);
                break
            }
            hset.clear();
        }
        hset.clear();
        for i in 0..ss.len() - 14 {
            hset.extend(ss[i..i+14].chars());
            if hset.len() == 14 {
                println!("{}", i + 14);
                break
            }
            hset.clear();
        }

    }
    return Ok(());
}