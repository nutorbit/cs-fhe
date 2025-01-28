import random


def generate_shares(secret, num_shares, threshold):
    """
    ref: https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing
    """
    coefficients = [secret] + [random.randint(1, 100) for _ in range(threshold - 1)]

    shares = []
    for i in range(1, num_shares + 1):
        x = i
        y = sum(c * (x ** idx) for idx, c in enumerate(coefficients))  # Polynomial evaluation
        shares.append((x, y))
    return shares


def reconstruct_secret(shares):
    x_values, y_values = zip(*shares)
    secret = 0

    for i in range(len(x_values)):
        numerator, denominator = 1, 1
        for j in range(len(x_values)):
            if i != j:
                numerator *= -x_values[j]
                denominator *= x_values[i] - x_values[j]

        lagrange_polynomial = numerator / denominator
        secret += y_values[i] * lagrange_polynomial

    return round(secret)


def main():
    alpha, beta, gamma = 0.6, 0.4, 0
    threshold = 2
    num_shares = 3

    scoreA = 700
    scoreB = 650
    scoreZ = 0

    # Step 1: Bank sends model M (weights) to all parties
    model = f"G = {alpha} * scoreA + {beta} * scoreB + {gamma} * scoreZ"
    print("Bank sends model to all parties:", model)

    # Step 2: Generate secret shares for each input
    sharesA = generate_shares(scoreA, num_shares, threshold)
    sharesB = generate_shares(scoreB, num_shares, threshold)
    sharesZ = generate_shares(scoreZ, num_shares, threshold)

    print("Shares for scoreA:", sharesA)
    print("Shares for scoreB:", sharesB)
    print("Shares for scoreZ:", sharesZ)

    # Step 3: Each party computes G using the shares
    partial_results = []
    for i in range(num_shares):
        scoreA_share = sharesA[i][1]
        scoreB_share = sharesB[i][1]
        scoreZ_share = sharesZ[i][1]

        G_share = alpha * scoreA_share + beta * scoreB_share + gamma * scoreZ_share
        partial_results.append((sharesA[i][0], G_share))

    # Step 4: Parties send their outputs to the Receiver
    print("Partial results sent to the Receiver:", partial_results)

    # Step 5: The Receiver decodes the output
    final_score = reconstruct_secret(partial_results)

    # Verify correctness
    expected_score = alpha * scoreA + beta * scoreB + gamma * scoreZ
    print("Expected credit score:", expected_score)
    print("Final credit score decoded by the Receiver:", final_score)
    assert final_score == expected_score, "The final score does not match the expected value"


if __name__ == "__main__":
    main()
