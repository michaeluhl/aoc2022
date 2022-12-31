use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::env;
use std::process;
use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};
use std::ops::{Add,Sub};


#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
struct Coord(i32, i32);

impl Sub for Coord {
    type Output = Coord;

    fn sub(self, rhs: Coord) -> Coord {
        Coord(self.0 - rhs.0, self.1 - rhs.1)
    }

}

impl Add for Coord {
    type Output = Coord;

    fn add(self, rhs: Coord) -> Coord {
        Coord(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl Coord {
    fn as_idx(self) -> Option<(usize, usize)> {
        if self.0 >= 0 && self.1 >= 0 {
            return Some((self.0 as usize, self.1 as usize))
        }
        None
    } 
}


#[derive(Clone, Copy, Debug)]
struct State {
    posn: Coord,
    dist: usize
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(other.dist.cmp(&self.dist))    
    }
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.dist.cmp(&self.dist)
    }
}

impl PartialEq for State {
    fn eq(&self, other: &Self) -> bool {
        self.dist == other.dist
    }
}

impl Eq for State {}


#[derive(Debug)]
struct Grid {
    data: Vec<Vec<i32>>,
    start: Coord,
    end: Coord
}


fn plot(grid: &Grid, start: &Coord, end: &Coord, prev: &HashMap<Coord,Coord>) {
    let (nr, nc): (usize, usize) = (grid.data.len(), grid.data[0].len());
    let mut disp: Vec<Vec<char>> = vec![vec!['.'; nc]; nr];

    if let Some((tj, ti)) = end.as_idx() {
        disp[tj][ti] = 'E';
    }

    let mut node: &Coord = end;
    while let Some(next) = prev.get(node)  {
        if let Some((nj, ni)) = next.as_idx() {
            let dctn = *node - *next;
            match dctn {
                Coord(-1, 0) => disp[nj][ni] = '^',
                Coord(1, 0) => disp[nj][ni] = 'v',
                Coord(0, 1) => disp[nj][ni] = '>',
                Coord(0, -1) => disp[nj][ni] = '<',
                _ => panic!("Invalid direction found.")
            }
        }
        node = next;
    }

    if let Some((tj, ti)) = start.as_idx() {
        disp[tj][ti] = 'S';
    }

    for row in disp.iter() {
        println!("{}", row.iter().collect::<String>());
    }

}


fn route(grid: &Grid, start: &Coord, end: Option<&Coord>) -> Option<(HashMap<Coord, usize>, HashMap<Coord, Coord>, Coord)> {
    let (nr, nc): (usize, usize) = (grid.data.len(), grid.data[0].len());
    let maxsize: usize = nr * nc;
    let mut dist_m: HashMap<Coord, usize> = HashMap::new();
    let mut prev_m: HashMap<Coord, Coord> = HashMap::new();
    let mut q: BinaryHeap<State> = BinaryHeap::new();
    let directions: [Coord; 4] = [Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1)];

    let e_check: Box<dyn Fn(&Coord) -> bool> = match end {
        Some(_end) => Box::new(|c: &Coord| -> bool {*c == *(end.unwrap())}),
        _ => Box::new(|c: &Coord| -> bool {
            if let Some((j, i)) = c.as_idx() {
                grid.data[j][i] == ('a' as i32)
            } else {
                false
            }
        })
    };

    let n_check: Box<dyn Fn(&Coord, &Coord) -> bool> = match end {
        Some(_end) => Box::new(|s: &Coord, o: &Coord| -> bool {
            if let (Some((oj, oi)), Some((sj, si))) = (o.as_idx(), s.as_idx()) {
                grid.data[oj][oi] - grid.data[sj][si] <= 1
            } else {
                false
            }
        }),
        _ => Box::new(|s: &Coord, o: &Coord| -> bool {
            if let (Some((oj, oi)), Some((sj, si))) = (o.as_idx(), s.as_idx()) {
                grid.data[oj][oi] - grid.data[sj][si] >= -1
            } else {
                false
            }
        })
    };

    let v_check = |c: &Coord| -> bool {
        if let Some((j, i)) = c.as_idx() {
            j < nr && i < nc
        } else {
            false
        }
    };

    dist_m.insert(start.clone(), 0);
    q.push(State{posn: start.clone(), dist: 0});

    while let Some(State{posn, dist}) = q.pop() {
        let &mut c_dist = dist_m.entry(posn).or_insert(maxsize);
        if c_dist < dist {continue;}
        for other in directions.iter()
                               .map(|d| posn + *d)
                               .filter(v_check) {
            if e_check(&posn) {
                return Some((dist_m, prev_m, posn));
            }
            if n_check(&posn, &other) {
                let o_dist = dist_m.entry(other).or_insert(maxsize);
                if c_dist + 1 < *o_dist {
                    q.push(State{posn: other, dist: c_dist + 1});
                    *o_dist = c_dist + 1;
                    prev_m.insert(other, posn);
                }
            }          
            
        }

    }

    println!("Did not find a route");

    return None;

}


fn load_data(filename: &str) -> io::Result<Grid> {
    let mut start: Option<Coord> = None;
    let mut end: Option<Coord> = None;
    let mut data: Vec<Vec<i32>> = Vec::new();

    let file = File::open(filename)?;
    let reader: BufReader<File> = BufReader::new(file);

    for (j, line_) in reader.lines().enumerate() {
        let line = line_.expect("Expecting a data line.");
        let mut chars: Vec<char> = line.chars().collect();
        let col = chars.iter().position(|&c| c == 'S');
        if let Some(c) = col {
            start = Some(Coord(j as i32, c as i32));
            chars[col.unwrap()] = 'a';
        }
        let col = chars.iter().position(|&c| c == 'E');
        if let Some(c) = col {
            end = Some(Coord(j as i32, c as i32));
            chars[col.unwrap()] = 'z';
        }
        data.push(chars.iter().map(|&c| c as i32).collect());
    }

    return Ok(Grid {
        data,
        start: start.unwrap(),
        end: end.unwrap()
    });
}


fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Expected a single argument: name of file to process.");
        process::exit(1);
    }

    let grid: Grid = load_data(&args[1])?;

    println!("Start: {:?}, End: {:?}", grid.start, grid.end);
    for row in grid.data.iter() {
        println!("{}", row.iter().map(|i| (*i as u8) as char).collect::<String>());
    }

    if let Some((dist, prev, nend)) = route(&grid, &(grid.start), Some(&(grid.end))) {
        println!("Part 1 Dist: {}", dist[&grid.end]);
        plot(&grid, &(grid.start), &nend, &prev);
    }

    println!("\n{}\n", vec!['-'; 50].iter().collect::<String>());

    if let Some((dist, prev, nend)) = route(&grid, &(grid.end), None) {
        println!("Part 2 Dist: {}", dist[&nend]);
        plot(&grid, &(grid.end), &nend, &prev);
    }

    return Ok(());
}