from concrete import fhe

from cs_fhe.circuits import CreditScoreAveraging


configuration = fhe.Configuration(
    enable_unsafe_features=True,
    use_insecure_key_cache=True,
    insecure_key_cache_location=".keys",
    show_progress=True,
    progress_tag=True,
    progress_title="Evaluation:",
)


def main():
    input_range = 20
    
    credit_score_averaging_fhe = CreditScoreAveraging.compile({
        "add": list(zip(range(0, input_range), range(0, input_range))),
        "half": list(range(0, input_range)),
    }, configuration)
    
    print("Generating keyset ...")
    credit_score_averaging_fhe.keygen()
    
    print("Encrypting initial values")
    x = 5
    y = 2
    
    # Add Operation
    (x_enc, y_enc) = credit_score_averaging_fhe.add.encrypt(x, y)
    u_enc = credit_score_averaging_fhe.add.run(x_enc, y_enc)
    
    # Half Operation
    v_enc = credit_score_averaging_fhe.half.run(u_enc)
    
    # Decrypting the result
    v = credit_score_averaging_fhe.half.decrypt(v_enc)
    
    print("Result: ", v)
    print("Expected: ", (x + y) // 2)
    
    assert v == (x + y) // 2, "The result does not match the expected value"
    
    
if __name__ == "__main__":
    main()
