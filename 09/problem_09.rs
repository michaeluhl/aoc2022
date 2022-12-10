use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::env;
use std::process;
use std::collections::HashMap;

#[derive(Debug)]
struct Node {
    x: i32,
    y: i32
}


impl Node {

    fn new() -> Node {
        Node {
            x: 0,
            y: 0
        }
    }
}

fn clip(x: i32, y: i32) -> (i32, i32) {
    if (x.abs() < 2) && (y.abs() < 2) {
        return (0, 0);
    }
    return (
        match x {
            0 => 0,
            _ => x/x.abs()
        },
        match y {
            0 => 0,
            _ => y/y.abs()
        }
    );
}


fn main() -> io::Result<()> {

    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        println!("problem_09 <num_nodes> <filename>");
        process::exit(1);
    }

    let cmds: HashMap<&str, (i32, i32)> = HashMap::from([
        ("L", (-1, 0)),
        ("R", (1, 0)),
        ("U", (0, 1)),
        ("D", (0, -1))
    ]);

    let nnodes: usize = args[1].parse::<usize>().expect("Expected an integer number of nodes");
    let mut nodes: Vec<Node> = Vec::new();

    for _i in 0..nnodes {
        nodes.push(Node::new());
    }

    let mut posns: HashMap<(i32, i32), i32> = HashMap::new();
    posns.insert((0,0), 0);

    let f: File = File::open(&args[2])?;
    let reader: BufReader<File> =  BufReader::new(f);

    for line_ in reader.lines() {
        let line = line_?;
        let (d, c) = line.split_once(" ").expect("Space delimited string");
        let ic:i32 = c.parse::<i32>().expect("Expected integer movement count");
        let (dx, dy) = cmds.get(d).unwrap();
        for _i in 0..ic {
            nodes[0].x += *dx;
            nodes[0].y += *dy;
            for j in 1_usize..nnodes {
                let mut distx: i32 = nodes[j - 1].x - nodes[j].x;
                let mut disty: i32 = nodes[j - 1].y - nodes[j].y;
                (distx, disty) = clip(distx, disty);
                if (distx != 0) || (disty != 0) {
                    nodes[j].x += distx;
                    nodes[j].y += disty;
                    if j == nnodes -1 {
                        let count = posns.entry((nodes[j].x, nodes[j].y)).or_insert(0);
                        *count += 1;
                    }
                }
            }
        }
    }

    println!("{}", posns.len());

    return Ok(());
}


