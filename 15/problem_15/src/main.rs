extern crate argparse;

use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use fnv::FnvHashSet;
use argparse::{ArgumentParser, Store};


fn draw_ball(posns: &mut FnvHashSet<(i32, i32)>, cx: i32, cy: i32, rad: i32, zone: i32) {
    for (j, i) in ((-1*rad)..1).zip(0..(rad + 1)) {
        posns.extend(
            [
                (cx + i, cy + j), 
                (cx + j, cy + i), 
                (cx - i, cy + j), 
                (cx - j, cy + i)
                ].iter().filter(|(x, y)| (0 <= *x) && (*x <= zone) && (0 <= *y) && (*y <= zone))
        );
    }
}


fn eval_line(sensors: &Vec<(i32, i32)>,
             beacons: &Vec<(i32, i32)>,
             radii: &Vec<i32>,
             linenum: i32) -> usize {
    let mut posns: FnvHashSet<i32> = FnvHashSet::default();
    for ((s, b), r) in sensors.iter().zip(beacons.iter()).zip(radii.iter()) {
        let diff = (linenum - s.1).abs();
        if diff <= *r {
            let hr = r - diff;
            posns.extend((s.0 - hr)..(s.0+hr+1));
        }
        if b.1 == linenum {
            posns.remove(&b.0);
        }
    }
    return posns.len();
} 


fn read_data(filename: &str,
             sensors: &mut Vec<(i32, i32)>,
             beacons: &mut Vec<(i32, i32)>,
             ) -> io::Result<()> {

    let input_file = File::open(filename)?;
    let reader: BufReader<File> = BufReader::new(input_file);
    let mut buffer: Vec<i32> = Vec::new();
    for line_ in reader.lines() {
        let line = line_.expect("Expected a data line");
        for half in line.split(":") {
            for coord in half.split(",") {
                let value = coord.split("=").last().expect("Integer").parse::<i32>().expect("Integer");
                buffer.push(value);
            }
        }
        sensors.push((buffer[0], buffer[1]));
        beacons.push((buffer[2], buffer[3]));
        buffer.clear();
    }
    return Ok(());
}


fn main() -> io::Result<()> {
    let mut grid_line: i32 = 2_000_000;
    let mut fname = "test.txt".to_string();
    let mut zone: i32 = -1;
    {
        let mut ap = ArgumentParser::new();
        ap.set_description("A program for AoC Day 15");
        ap.refer(&mut grid_line).add_option(&["-N", "--number"], Store, "Grid line to process");
        ap.refer(&mut zone).add_option(&["-z", "--zone"], Store, "Zone (limit) to process");
        ap.refer(&mut fname).add_argument("INPUT", Store, "Input file to process").required();

        ap.parse_args_or_exit();
    }

    let mut sensors: Vec<(i32, i32)> = Vec::new();
    let mut beacons: Vec<(i32, i32)> = Vec::new();

    {
        let _ = read_data(&fname, &mut sensors, &mut beacons);
    }

    let radii = sensors.iter()
                                 .zip(beacons.iter())
                                 .map(|(s, b)| (b.0 - s.0).abs() + (b.1 - s.1).abs())
                                 .collect();
    let unavail = eval_line(&sensors, &beacons, &radii, grid_line);
    println!("{}", unavail);

    if zone > 0 {
        let mut posns: FnvHashSet<(i32, i32)> = FnvHashSet::default();
        for (&(sx, sy), &srad) in sensors.iter().zip(radii.iter()) {
            draw_ball(&mut posns, sx, sy, srad + 1, zone);
        }
        println!("Found {} potential positions.", posns.len());
        let mut cull: FnvHashSet<(i32, i32)> = FnvHashSet::default();
        for (&(cx, cy), &crad) in sensors.iter().zip(radii.iter()) {
            cull.extend(posns.iter().filter(|(tx, ty)| (*tx - cx).abs() + (*ty - cy).abs() <= crad))
        }
        let remnant: FnvHashSet<_> = posns.difference(&cull).collect();
        println!("{}", remnant.len());
        for (fx, fy) in remnant.iter() {
            println!("Result: {}, {}", *fx, *fy);
            println!("Result: {}", (4_000_000*(*fx as i64) + (*fy as i64)));
        }
    }

    return Ok(())
}
