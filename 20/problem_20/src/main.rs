extern crate argparse;

use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::env;
use argparse::{ArgumentParser, Store};


#[derive(Clone, Copy, Debug)]
struct RingNode {
    value: i64,
    prev: usize,
    next: usize
}


struct OrderableRing {
    values: Vec<RingNode>
}


impl OrderableRing {

    fn new() -> OrderableRing {
        OrderableRing { values: Vec::new() }
    }

    fn len(&self) -> usize {
        self.values.len()
    }

    fn push(&mut self, value: i64) {
        let idx = self.values.len();
        self.values.push(
            RingNode {
                value,
                prev: if idx >= 1 {idx-1} else {0},
                next: 0
            }
        );
        if idx >= 1 {
            if let Some(p) = self.values.get_mut(idx - 1) {
                p.next = idx;
            }
        } 
    }

    fn enclose(&mut self) {
        let len = self.values.len() - 1;
        if let Some(fl) = self.values.first_mut() { fl.prev = len; }
    }

    fn traverse(&self, start: usize, count: usize) -> usize {
        let mut p = start;
        for _ in 0..count {
            if let Some(n) = self.values.get(p) {
                p = n.next;
            }
        }
        return p;
    }

    fn mv(&mut self, start: usize, modulo: usize) {
        let value:i64 = if let Some(sn) = self.values.get(start) { sn.value } else { 0 };
        let count:usize = if modulo > 0 { value.abs() as usize % modulo } else { value.abs() as usize };
        for _ in 0..count {
            let (mut pi, mut si, mut ni): (usize, usize, usize) = (0, 0, 0);
            if value < 0 {
                let cn = self.values.get(start).unwrap();
                (si, ni) = (cn.prev, cn.next);
                {
                    let mut swap = self.values.get_mut(si).unwrap();
                    pi = swap.prev;
                    swap.prev = start;
                    swap.next = ni;
                }
                {
                    let mut cnm = self.values.get_mut(start).unwrap();
                    cnm.prev = pi;
                    cnm.next = si;
                }
                // Next
                self.values.get_mut(ni).unwrap().prev = si;
                // Prev
                self.values.get_mut(pi).unwrap().next = start;
            } else {
                let cn = self.values.get(start).unwrap();
                (pi, si) = (cn.prev, cn.next);
                {
                    let mut swap = self.values.get_mut(si).unwrap();
                    ni = swap.next;
                    swap.prev = pi;
                    swap.next = start;
                }
                {
                    let mut cnm = self.values.get_mut(start).unwrap();
                    cnm.prev = si;
                    cnm.next = ni;
                }
                // Prev
                self.values.get_mut(pi).unwrap().next = si;
                // Next
                self.values.get_mut(ni).unwrap().prev = start;
            }
        }    
    }

    fn print(&self) {
        for n in self.values.iter() {
            println!("{:?}", n);
        }
    }
}


fn main() -> io::Result<()> {

    let mut key: i64 = 1;
    let mut mixes: usize = 1;
    let mut fname = "input.txt".to_string();

    {
        let mut ap = ArgumentParser::new();
        ap.set_description("Program for AoC 2022 Problem 20");
        ap.refer(&mut key).add_option(&["-k", "--key"], Store, "Decryption key (defaults to 1)");
        ap.refer(&mut mixes).add_option(&["-m", "--mixes"], Store, "Number of times that mixing should be performed.");
        ap.refer(&mut fname).add_argument("INPUT", Store, "Input file to process").required();

        ap.parse_args_or_exit();
    }


    let file: File = File::open(&fname)?;
    let reader: BufReader<File> = BufReader::new(file);
    let mut llist: OrderableRing = OrderableRing::new();

    let mut zidx: Option<usize> = None;
    
    for (i, line_) in reader.lines().enumerate() {
        let line: String = line_?;
        let v = line.parse::<i64>().unwrap() * key;
        llist.push(v);
        if v == 0 {
            zidx = Some(i);
        }
    }
    llist.enclose();

    let lv = llist.len() - 1;
    println!("Shifting mod {}", lv);
    for _ in 0..mixes {
        for i in 0..llist.len() {
            llist.mv(i, lv)
        }
    }

    if let Some(start) = zidx {
        let mut sum: i64 = 0;
        let mut v: usize = start;
        for _ in 0..3 {
            v = llist.traverse(v, 1000);
            println!("{}", llist.values.get(v).unwrap().value);
            sum += llist.values.get(v).unwrap().value;
        }
        println!("Sum: {}", sum);    
    }

    Ok(())
}