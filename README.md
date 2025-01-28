# Credit Score with Fully Homomorphic Encryption

This repository contains the implementation of a credit score system using Fully Homomorphic Encryption (FHE).

## Setup

### Python

We use [poetry](https://python-poetry.org/) to manage dependencies. To install the dependencies, run:

```bash
poetry install
```

To activate the virtual environment, run:

```bash
poetry shell
```

### Rust

We use [Cargo](https://doc.rust-lang.org/cargo/) to manage dependencies. To install the dependencies, run:

```bash
cd rust/fhe
cargo build
```

To run the code, run:

```bash
cargo run --release
```

Drop the `--release` flag if you want to run the code in debug mode.