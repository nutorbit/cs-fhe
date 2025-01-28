mod fhe;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    _ = fhe::sim_fhe();
    Ok(())
}
