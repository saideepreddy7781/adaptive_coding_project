# 🛰️ Adaptive Coding & Modulation Simulation (LDPC & Polar)

This project simulates-high performance **Adaptive Coding and Modulation (ACM)** using **LDPC** and **Polar Codes** over a Rayleigh Fading Channel. It compares these advanced schemes against a fixed-rate baseline and Uncoded BPSK.

## 🚀 Quick Start (Fresh Laptop)

Follow these steps to set up and run the simulation on any computer with Python 3 installed.

### 1. Set Up the Environment
Open your terminal in the project folder and run:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install all requirements
pip install -r requirements.txt
```

### 2. Run the Simulation
To execute the simulation and generate all 8 performance graphs at once:

```bash
python adaptive_coding_project/main.py
```

---

## 📊 Generated Results
After running, the `results/` folder will contain the following 8 plots:

1.  **`proposal_ber.png`**: BER vs SNR for LDPC/Polar Comparison.
2.  **`ber_plot_adaptive.png`**: Dedicated BER plot for the Adaptive scheme.
3.  **`proposal_throughput.png`**: Throughput vs SNR (Normalized & Stepwise).
4.  **`bler_realistic.png`**: Block Error Rate (BLER) for Multi-Rate codes.
5.  **`ber_plot.png` & `ber_realistic.png`**: Standard/Legacy BER comparisons.
6.  **`throughput_plot.png` & `throughput_realistic.png`**: Standard/Legacy Throughput comparisons.

## 🛠️ Requirements
- Python 3.8+
- libraries: `numpy`, `matplotlib`, `pyldpc`, `numba`, `scipy`

---
*Developed for research into Adaptive Coding and Modulation schemes.*
