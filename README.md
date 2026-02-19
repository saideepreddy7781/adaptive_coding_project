# Adaptive Coding Simulation (LDPC & Polar)

This project simulates the performance of **Adaptive Coding and Modulation (ACM)** using **LDPC** (Low-Density Parity-Check) and **Polar Codes**. The simulation compares these advanced coding schemes against Uncoded BPSK transmission over a **Rayleigh Fading Channel**.

## Features

- **Channel Model**: Rayleigh Fading with Additive White Gaussian Noise (AWGN).
- **Modulation**: Binary Phase Shift Keying (BPSK).
- **Coding Schemes**:
  - **LDPC Codes**: Rates 1/3, 1/2, 3/4.
  - **Polar Codes**: Rates 1/3, 1/2, 3/4 (constructed using Bhattacharyya bounds).
  - **Uncoded**: Baseline BPSK.
  - **Adaptive (ACM)**: Dynamically selects the best coding scheme based on the effective SNR to maximize throughput while maintaining low Block Error Rate (BLER).
- **Metrics**: Bit Error Rate (BER), Block Error Rate (BLER), and Throughput.

## Requirements

The project implementation relies on the following Python libraries:

- `numpy`
- `matplotlib`
- `pyldpc` (for LDPC code construction and decoding)

## Installation

1. Clone or download the repository.
2. Install the required dependencies:

```bash
pip install numpy matplotlib pyldpc
```

## Usage

To run the simulation and generate performance plots:

```bash
python adaptive_coding_project/main.py
```

*Note: The simulation may take some time depending on the number of frames and SNR points.*

## Output

The simulation generates the following plots in the `results/` directory:

- `proposal_ber.png`: BER vs SNR comparison.
- `proposal_throughput.png`: Throughput vs SNR comparison.

## Project Structure

- `adaptive_coding_project/`: Source code package.
  - `main.py`: Main entry point for the simulation.
  - `channel.py`: Channel models (Rayleigh, AWGN).
  - `modulation.py`: Modulation and Demodulation (BPSK).
  - `ldpc_coding.py`: Wrapper for `pyldpc` functions.
  - `polar_coding.py`: Implementation of Polar Code construction, encoding, and SC decoding.
  - `utils.py`: Utility functions.
