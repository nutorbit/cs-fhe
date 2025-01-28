use std::io::Cursor;
use tfhe::prelude::*;
use tfhe::{generate_keys, set_server_key, ConfigBuilder, FheUint32, FheUint8, ServerKey};

fn server_function(serialized_data: &[u8]) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    let mut serialized_data = Cursor::new(serialized_data);
    let server_key: ServerKey = bincode::deserialize_from(&mut serialized_data)?;
    let encrypted_score_a: FheUint32 = bincode::deserialize_from(&mut serialized_data)?;
    let encrypted_score_b: FheUint32 = bincode::deserialize_from(&mut serialized_data)?;
    let encrypted_alpha: FheUint8 = bincode::deserialize_from(&mut serialized_data)?;
    let encrypted_beta: FheUint8 = bincode::deserialize_from(&mut serialized_data)?;

    set_server_key(server_key);

    // Perform the homomorphic computation
    let weighted_score_a = &encrypted_score_a * &encrypted_alpha.cast_into();
    let weighted_score_b = &encrypted_score_b * &encrypted_beta.cast_into();
    let encrypted_sum = &weighted_score_a + &weighted_score_b;

    // Serialize the result to send back to the client
    let serialized_result = bincode::serialize(&encrypted_sum)?;

    Ok(serialized_result)
}

pub fn sim_fhe() -> Result<(), Box<dyn std::error::Error>> {
    // Configuration and Key Generation
    let config = ConfigBuilder::default().build();
    let (client_key, server_key) = generate_keys(config);

    // Inputs for MPC with Threshold FHE
    let clear_score_a = 800u32; // Teleco A's input
    let clear_score_b = 700u32; // Bank B's input
    let clear_alpha = 6u8; // Weight for score_a
    let clear_beta = 4u8; // Weight for score_b

    // Encrypt the inputs using the client key
    let encrypted_score_a = FheUint32::encrypt(clear_score_a, &client_key);
    let encrypted_score_b = FheUint32::encrypt(clear_score_b, &client_key);
    let encrypted_alpha = FheUint8::encrypt(clear_alpha, &client_key);
    let encrypted_beta = FheUint8::encrypt(clear_beta, &client_key);

    // Serialize data to send to the server
    let mut serialized_data = Vec::new();
    bincode::serialize_into(&mut serialized_data, &server_key)?;
    bincode::serialize_into(&mut serialized_data, &encrypted_score_a)?;
    bincode::serialize_into(&mut serialized_data, &encrypted_score_b)?;
    bincode::serialize_into(&mut serialized_data, &encrypted_alpha)?;
    bincode::serialize_into(&mut serialized_data, &encrypted_beta)?;

    // Simulate server-side computation
    let serialized_result = server_function(&serialized_data)?;
    let encrypted_result: FheUint32 = bincode::deserialize(&serialized_result)?;

    // Decrypt the result on the client side
    let decrypted_result: u32 = encrypted_result.decrypt(&client_key);
    println!("Decrypted Weighted Sum: {}", decrypted_result);

    Ok(())
}
