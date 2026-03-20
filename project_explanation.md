# 🚀 Step-by-Step Guide: Adaptive Coding Simulation

Hello! This project is a simulation of how modern wireless communication (like 4G, 5G, or Wi-Fi) sends data reliably through "air" (the channel) even when there is noise and interference.

---

## 🛠️ Phase 1: Preparation (The Setup)
Before running anything, make sure your computer has the "tools" needed to understand the code.

1.  **Install Python:** Ensure you have Python installed on your system.
2.  **Open Terminal:** Open your Command Prompt, Terminal, or PowerShell.
3.  **Install Libraries:** These are pre-written codes that help us with math (`numpy`), drawing graphs (`matplotlib`), and complex error-correction math (`pyldpc`).
    ```bash
    pip install numpy matplotlib pyldpc
    ```

---

## 🏃 Phase 2: Running the Project
Now, we tell the computer to start the "Experiment."

1.  **Execute the Script:** Run this command in your terminal from the project's root folder:
    ```bash
    python adaptive_coding_project/main.py
    ```
2.  **Watch the Progress:** You will see text appearing in your terminal. It will show different **SNR levels** (Signal-to-Noise Ratio). 
    - **Think of SNR as "Volume":** High SNR means the signal is loud and clear (like standing next to someone); Low SNR means it's very noisy (like a crowded party).

---

## 🧠 Phase 3: What happens "Under the Hood"?
When you run `main.py`, here is what the computer is doing step-by-step:

### 1. Generating the "Secret Codes"
The program creates **LDPC** and **Polar** codes. These are mathematical recipes for adding "extra" bits to your data. If some bits get lost in the air, these extra bits help the receiver "guess" what was missing.

### 2. The Loop (Trial and Error)
The program tests 13 different "Volume" levels (from 0dB to 12dB). For each level, it:
- **Picks a Gear (Adaptive Coding):** If the signal is clear, it sends data fast (Rate 3/4). If it's noisy, it slows down to send data very safely (Rate 1/3).
- **Simulates Communication:** It sends 1s and 0s through a virtual "Rayleigh Fading Channel" (which simulates real-world obstacles like walls or distance).
- **Detects Errors:** It counts how many 1s turned into 0s and vice-versa.

### 3. Calculating Success Metrics
- **BER (Bit Error Rate):** What percentage of bits were wrong? (Lower is better!)
- **Throughput:** How much actual "useful" information got through per second? (Higher is better!)

---

## 📊 Phase 4: Seeing the Results
Once finished, the program creates a folder named `results/` containing two pictures:

1.  **`proposal_ber.png`**: This graph shows that as the signal gets louder (SNR increases), the errors (BER) drop significantly. 
2.  **`proposal_throughput.png`**: This is the "Speed" graph. It shows that as the signal improves, the "Adaptive" mode automatically switches to higher speeds!

---

## 🎉 Summary for Your Friend
"This project is like testing a walkie-talkie. We start in a noisy room and slowly walk closer to each other. The code automatically adjusts how fast I speak so you can always understand me, even when it's noisy. Then, it draws a graph to prove that 'Adaptive' speaking is better than just talking at one speed!"
