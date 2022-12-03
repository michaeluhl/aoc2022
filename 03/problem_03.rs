use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::collections::HashSet;
use std::convert::TryFrom;


fn priority(chars: &HashSet<char>) -> i32 {
    let mut priority: i32 = 0;
    let mut ord: i32 = 0;
    for c in chars {
        ord = i32::try_from((*c) as u32).unwrap();
        match c.is_uppercase() {
            true => priority += ord - 38,
            false => priority += ord - 96
        }
    }
    return priority;
}


fn main() -> io::Result<()> {
    let mut total_priority: i32 = 0;
    let mut group_priority: i32 = 0;
    let mut group_set: HashSet<char> = HashSet::new();

    let f: File = File::open("input.txt")?;
    let reader: BufReader<File> = BufReader::new(f);

    for (i, line_) in reader.lines().enumerate() {
        let hold = line_?; 
        let line: &str = hold.trim();
        if i % 3 == 0 {
            if group_set.len() > 0 {
                group_priority += priority(&group_set);
                group_set.clear();
            }
            group_set.extend(line.chars());
        }
        let line_set: HashSet<char> = line.chars().collect();
        group_set.retain(|c| line_set.contains(c));
        let hlen: usize = line.len() / 2;
        let comp1: HashSet<char> = line[..hlen].chars().collect();
        let comp2: HashSet<char> = line[hlen..].chars().collect();
        let common: HashSet<char> = &comp1 & &comp2;
        total_priority += priority(&common); 
    }
    if group_set.len() > 0 {
        group_priority += priority(&group_set);
    }

    println!("{}", total_priority);
    println!("{}", group_priority);

    return Ok(());

}