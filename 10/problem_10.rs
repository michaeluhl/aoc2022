use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::env;
use std::process;

#[derive(Debug)]
struct Cmd {
    inst: String,
    arg: Option<i32>
}


impl Cmd {

    fn new(inst: String) -> Cmd {
        Cmd {
            inst: inst,
            arg: None
        }
    }

    fn new_with_arg(inst: String, arg: i32) -> Cmd {
        Cmd {
            inst: inst,
            arg: Some(arg)
        }
    }
}


fn main() -> io::Result<()> {

    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Must supply filename");
        process::exit(1);
    }

    println!("Read args");

    let f: File = File::open(&args[1])?;
    let reader: BufReader<File> = BufReader::new(f);

    let mut program: Vec<Cmd> = Vec::new();
    for line_ in reader.lines() {
        let line = line_?;
        if let Some((inst, arg)) = line.split_once(" ") {
            program.push(Cmd::new_with_arg(inst.to_string(), arg.parse::<i32>().unwrap()));
        } else {
            program.push(Cmd::new(line));
        }
    }

    println!("Read program");

    let mut x: i32 = 1;
    let mut ip: usize = 0;
    let mut tc: i32 = 0;
    let mut ic: i32 = 0;

    let mut sig: Vec<i32> = Vec::new();
    let mut crt: Vec<Vec<char>> = Vec::new();
    crt.push(Vec::new());

    loop {
        tc += 1;
        if ic == 0 {
            let cmd: &Cmd = program.get(ip).unwrap();
            ic = match cmd.inst.as_str() {
                "addx" => 2,
                "noop" => 1,
                _ => 1 
            };
        }
        ic -= 1;
        if (tc -20) % 40 == 0 {
            sig.push(tc * x);
        }
        let pos = (tc -1) % 40;
        if ((x -1) <= pos) && (pos <= (x + 1)) {
            crt.last_mut().unwrap().push('#');
        } else {
            crt.last_mut().unwrap().push('.');
        }
        if crt.last().unwrap().len() == 40 {
            crt.push(Vec::new());
        }
        if ic == 0 {
            let cmd: &Cmd = program.get(ip).unwrap();
            if cmd.inst == "addx" {
                x += cmd.arg.unwrap();
            }
            ip += 1;
            if ip == program.len() {
                break;
            }
        }
    }

    println!("{:#?}", sig);
    println!("{}", sig.iter().sum::<i32>());

    for row in crt.iter() {
        let s: String = row.into_iter().collect();
        println!("{}", s);
    }

    Ok(())
}