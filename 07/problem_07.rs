use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::collections::HashMap;
use std::env;
use std::process;


#[derive(Debug, Default)]
struct Node {
    children: HashMap<String, Node>,
    size: i32
}

impl Node {
    fn new_file(&mut self, name: String, size: i32) {
        self.children.insert(
            name,
            Node {
                children: HashMap::new(),
                size: size
            }
        );
    }

    fn new_dir(&mut self, name: String) {
        self.children.insert(
            name,
            Node {
                children: HashMap::new(),
                size: 0
            }
        );
    }

    fn get_path(&mut self, path: &Vec<String>) -> Option<&mut Node> {
        let mut node = self;
        for part in path.iter() {
            if let Some(child) = node.children.get_mut(part) {
                node = child;
            } else {
                return None;
            }
        }
        Some(node)
    }

}


fn main() -> io::Result<()> {

    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Expected the file name as an argument.");
        process::exit(1);
    }

    let mut root: Node = Node {
        children: HashMap::new(),
        size: 0
    };

    let mut dir_path: Vec<String> = Vec::new();
    let mut dir_size: Vec<i32> = Vec::new();

    let f: File = File::open(&args[1])?;
    let reader: BufReader<File> = BufReader::new(f);

    for line_ in reader.lines() {
        let line = line_?;

        if line.starts_with("$ cd /") {
            dir_path.clear();
        } else if line.starts_with("$ cd") {
            let (_, path) = line.rsplit_once(" ").unwrap();
            if path == ".." {
                let last_size: i32 = root.get_path(&dir_path).expect("Dir Ent").size;
                dir_path.pop();
                root.get_path(&dir_path).expect("Dir Ent").size += last_size;
                dir_size.push(last_size);
            } else {
                dir_path.push(path.to_string());
            }
        } else if !line.starts_with("$ ls"){
            let (val, name): (&str, &str) = line.split_once(" ").unwrap();
            if val == "dir" {
                root.get_path(&dir_path).expect("Dir Ent").new_dir(name.to_string());
            } else {
                let size: i32 = val.parse::<i32>().expect("Expected integer");
                root.get_path(&dir_path).expect("Dir Ent").new_file(name.to_string(), size);
                root.get_path(&dir_path).expect("Dir Ent").size += size;
            }
        }

    }
    while dir_path.len() > 0 {
        let last_size: i32 = root.get_path(&dir_path).expect("Dir Ent").size;
        dir_path.pop();
        root.get_path(&dir_path).expect("Dir Ent").size += last_size;
        dir_size.push(last_size);
    }
    dir_size.push(root.size);

    println!("Total Size: {}", root.size);
    println!(
        "Sum of Small Dirs: {}", 
        dir_size.iter().filter(|&x| x.le(&100000)).sum::<i32>()
    );
    
    let total_space = 70000000;
    let required_space = 30000000;
    let free_space = total_space - root.size;
    let need_space = required_space - free_space;
    println!("Needed Space: {}", need_space);
    
    if let Some(s) = dir_size.iter().filter(|&x| x.ge(&need_space)).min() {
        println!("Deletion Size: {}", s);
    }
    
    return Ok(());

}