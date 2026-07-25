mod config;
mod logger;
mod events;
mod plugins;
mod utils;

fn main() {
    println!("=================================");
    println!("        ECLYPSA Core");
    println!("=================================");
    println!("Version : 0.1.0-dev");
    println!("Status  : Bootstrapping...");
    println!("Platform: Rust");
    println!("=================================");

    logger::init();
    config::load();

    println!("Core initialized successfully.");
}
