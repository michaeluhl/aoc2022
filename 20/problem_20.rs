use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::collections::HashMap;
use std::env;

#[derive(Clone, Copy, Debug)]
struct Link {
    value: i32,
    prev: Option<i32>,
    next: Option<i32>
}


struct FauxLL {
    values: Vec<Link>,
    index: HashMap<i32, usize>
}


impl FauxLL {

    fn new() -> FauxLL {
        FauxLL {
            values: Vec::new(),
            index: HashMap::new()
        }
    }

    fn len(&self) -> usize {
        self.values.len()
    }

    fn push(&mut self, value: i32) {
        let idx = self.values.len();
        let pl = self.values.last();
        self.values.push(
            Link {
                value,
                prev: pl.map(|l| l.value),
                next: None
            }
        );
        self.index.insert(value, idx); //entry(value).insert_entry(idx);
        if let Some(p) = pl {
            p.next = Some(value);
        }
    }

    fn enclose(&mut self) {
        if let (Some(fl), Some(ll)) = (self.values.first_mut(), self.values.last_mut()) {
            fl.prev = Some(ll.value);
            ll.next = Some(fl.value);
        }
    }

    fn retr_mut(&mut self, value: Option<i32>) -> Option<&mut Link> {
        if let Some(v) = value {
            if let Some(idx) = self.index.get(&v) {
                self.values.get_mut(*idx)
            } else {
                None
            }
        } else {
            None
        }
    }

    fn retr(&self, value: Option<i32>) -> Option<&Link> {
        if let Some(v) = value {
            if let Some(idx) = self.index.get(&v) {
                self.values.get(*idx)
            } else {
                None
            }
        } else {
            None
        }
    }

    fn traverse(&self, start: i32, count: usize) -> Option<i32> {
        let mut p = self.retr(Some(start));
        for _ in 0..count {
            p = p.map(|l| self.retr(l.next).unwrap());
        }
        p.map(|l| l.value)
    }

    fn mv(&mut self, value: i32, modulo: usize) {
        let count = if modulo > 0 { value.abs() as usize % modulo } else { value.abs() as usize };
        if let Some(cl) = self.retr_mut(Some(value)) {
            for _ in 0..count {
                if value < 0 {
                    if let (Some(swap), Some(next)) = (self.retr_mut(cl.prev), self.retr_mut(cl.next)) {
                        let prev = self.retr_mut(swap.prev).unwrap();
                        cl.prev = Some(prev.value);
                        prev.next = Some(cl.value);
                        cl.next = Some(swap.value);
                        swap.prev = Some(cl.value);
                        swap.next = Some(next.value);
                        next.prev = Some(swap.value);
                    }
                } else {
                    if let (Some(prev), Some(swap)) = (self.retr_mut(cl.prev), self.retr_mut(cl.next)) {
                        let next = self.retr_mut(swap.next).unwrap();
                        swap.prev = Some(prev.value);
                        prev.next = Some(swap.value);
                        swap.next = Some(cl.value);
                        cl.prev = Some(swap.value);
                        cl.next = Some(next.value);
                        next.prev = Some(cl.value);
                    }
                }
            }    
        }
    }
}


fn main() -> io::Result<()> {

    let args: Vec<String> = env::args().collect();
    let mixes: usize = 1;

    let file: File = File::open(args.last().unwrap())?;
    let reader: BufReader<File> = BufReader::new(file);
    let mut llist: FauxLL = FauxLL::new();

    for (i, line_) in reader.lines().enumerate() {
        let line: String = line_?;
        let v = line.parse::<i32>().unwrap();
        llist.push(v);
    }
    llist.enclose();

    let lv = llist.len() - 1;
    println!("Shifting mod {}", lv);
    for _ in 0..mixes {
        for v in llist.values.iter() {
            llist.mv(v.value, 0);
        }

    }

    let mut sum: i32 = 0;
    let mut v: i32 = 0;
    for _ in 0..3 {
        v = llist.traverse(v, 1000).unwrap();
        println!("{}", v);
        sum += v
    }
    println!("Sum: {}", sum);

    Ok(())
}