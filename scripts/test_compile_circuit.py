from cs_fhe.circuits import CreditScoreAveraging


input_range = 10
input_set = range(0, input_range)
circuit = CreditScoreAveraging.compile({
    "bank": list(input_set),
    "telco": list(input_set),
    "add": list(zip(input_set, input_set)),
    "half": list(input_set)
})
circuit.server.save("server.zip")