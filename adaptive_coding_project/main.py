import numpy as np
import matplotlib.pyplot as plt
import os
import time
from utils import calculate_ber
from modulation import BPSKModulator
from channel import RayleighChannel
from ldpc_coding import create_ldpc_code, encode, decode, get_message
from polar_coding import construct_polar_code, polar_encode, polar_decode

def simulate_channel(tx_bits, snr_db, return_soft=False, code_rate=1.0):
    """
    Simulates transmission of bits over the channel.
    """
    modulator = BPSKModulator()
    channel = RayleighChannel()
    
    snr_linear = 10**(snr_db / 10.0)
    # Noise variance for LLRs: sigma^2 = 1 / (2 * R * Eb/N0)
    noise_variance = 0.5 / (snr_linear * code_rate)
    
    # 1. Modulate
    symbols = modulator.modulate(tx_bits)
    
    # 2. Channel (Rayleigh Fading + AWGN)
    # Pass symbol SNR (Es/N0) to channel
    es_n0_db = snr_db + 10 * np.log10(code_rate)
    received_signal, h = channel.apply_channel(symbols, es_n0_db)
    
    # 3. Demodulate
    rx_output = modulator.demodulate(received_signal, channel_gains=h, 
                                     noise_variance=noise_variance, 
                                     return_soft=return_soft)
    
    return rx_output

def simulate_frame_error_rate(snr_db, max_frames, min_errors, coding_scheme, rate, ldpc_params=None, polar_params=None):
    """
    Simulates Block Error Rate (BLER) and BER for a specific scheme at a specific SNR.
    
    Args:
        snr_db: SNR Point.
        max_frames: Maximum frames to simulate.
        min_errors: Minimum block errors to stop simulation.
        coding_scheme: 'ldpc' or 'polar'.
        rate: Code rate (approximate).
        
    Returns:
        ber, bler, effective_rate
    """
    
    # Setup Code
    H, G = None, None
    frozen_mask = None
    k, n = 0, 0
    effective_rate = 0.0
    
    if coding_scheme == 'ldpc':
        n = 600 # Use fixed n for LDPC
        d_v, d_c = ldpc_params['dv'], ldpc_params['dc']
        # Note: We rely on pre-computed or passed params to avoid re-generating matrices every frame
        # But here we might generate once per SNR point if passed as None, or expect them passed.
        # Ideally, we generate once outside. But for simplicity in this function, we do it here if needed.
        # Optimization: Generate outside!
        pass 
    elif coding_scheme == 'polar':
        n = 512 # Power of 2 for Polar
        k = int(n * rate)
        effective_rate = k / n
        # specific optimization: generate mask once
        pass

    # ... Actually, better to pass the CODE OBJECTS to avoid overhead ...
    
    return 0, 0, 0

def get_simulation_results():
    """
    Main execution of the simulation.
    """
    
    # Simulation Parameters
    snr_range_db = np.arange(0, 13, 1) # 0 to 12 dB
    max_frames = 200
    min_block_errors = 5 # Stop if we hit this many errors (for speed, realistic would be 100)
    
    # Define Schemes
    # LDPC Rates: ~1/3, ~1/2, ~3/4
    # Polar Rates: 1/3, 1/2, 3/4
    
    schemes = [
        {'type': 'uncoded', 'rate': 1.0, 'label': 'Uncoded'},
        {'type': 'ldpc', 'rate': 1/3, 'label': 'LDPC R=1/3'},
        {'type': 'ldpc', 'rate': 1/2, 'label': 'LDPC R=1/2'},
        {'type': 'ldpc', 'rate': 3/4, 'label': 'LDPC R=3/4'},
        {'type': 'polar', 'rate': 1/3, 'label': 'Polar R=1/3'},
        {'type': 'polar', 'rate': 1/2, 'label': 'Polar R=1/2'},
        {'type': 'polar', 'rate': 3/4, 'label': 'Polar R=3/4'},
    ]
    
    # Pre-generate Codes
    print("Generating Codes...")
    for s in schemes:
        if s['type'] == 'ldpc':
            n = 600
            H, G = create_ldpc_code(n, rate=s['rate'])
            s['H'] = H
            s['G'] = G
            s['k'] = G.shape[1]
            s['n'] = n
            s['real_rate'] = s['k'] / s['n']
            print(f"  {s['label']}: k={s['k']}, n={s['n']}, Rate={s['real_rate']:.2f}")
            
        elif s['type'] == 'polar':
            n = 512
            k = int(n * s['rate'])
            mask = construct_polar_code(n, k, design_snr_db=0.0)
            s['frozen_mask'] = mask
            s['k'] = k
            s['n'] = n
            s['real_rate'] = k / n
            print(f"  {s['label']}: k={s['k']}, n={s['n']}, Rate={s['real_rate']:.2f}")

        elif s['type'] == 'uncoded':
            s['k'] = 1000 # Block size for uncoded
            s['n'] = 1000
            s['real_rate'] = 1.0
            print(f"  {s['label']}: k={s['k']}, n={s['n']}, Rate={s['real_rate']:.2f}")

    # Store results
    results = {s['label']: {'ber': [], 'bler': [], 'throughput': []} for s in schemes}
    results['Adaptive'] = {'ber': [], 'bler': [], 'throughput': [], 'mode': []}
    
    print("\nStarting Monte-Carlo Simulation...")
    print(f"{'SNR':<5} | {'Scheme':<12} | {'BER':<10} | {'BLER':<10} | {'Thpt':<8} | {'Frames':<6}")
    print("-" * 65)

    for snr in snr_range_db:
        
        # 1. Run Fixed Schemes
        scheme_metrics = {} 
        
        for s in schemes:
            total_bit_errors = 0
            total_bits = 0
            block_errors = 0
            frames = 0
            
            while (frames < max_frames) and (block_errors < min_block_errors):
                tx_msg = np.random.randint(0, 2, s['k'])
                
                if s['type'] == 'ldpc':
                    tx_code = encode(s['G'], tx_msg)
                elif s['type'] == 'polar':
                    tx_code = polar_encode(tx_msg, s['frozen_mask'])
                else: # Uncoded
                    tx_code = tx_msg # Identity
                
                # Channel
                # For Uncoded, rate is 1.0. For others, it's < 1.0.
                rx_output = simulate_channel(tx_code, snr, return_soft=(s['type']!='uncoded'), code_rate=s['real_rate'])
                
                if s['type'] == 'ldpc':
                    rx_code_est = decode(s['H'], rx_output, snr) 
                    rx_msg_est = get_message(s['G'], rx_code_est)
                elif s['type'] == 'polar':
                    rx_msg_est = polar_decode(rx_output, s['frozen_mask'])
                else: # Uncoded: rx_output are hard bits (0/1) if return_soft=False
                    rx_msg_est = rx_output
                
                if len(rx_msg_est) != len(tx_msg):
                    errors = s['k'] // 2
                    is_block_error = True
                else:
                    errors = np.sum(tx_msg != rx_msg_est)
                    is_block_error = errors > 0
                
                total_bit_errors += errors
                block_errors += int(is_block_error)
                total_bits += s['k']
                frames += 1
            
            # Compute Metrics
            ber = total_bit_errors / total_bits
            bler = block_errors / frames if frames > 0 else 0
            throughput = s['real_rate'] * (1 - bler)
            
            results[s['label']]['ber'].append(ber)
            results[s['label']]['bler'].append(bler)
            results[s['label']]['throughput'].append(throughput)
            
            # Only consider Coded schemes for Adaptive Logic candidates
            if s['type'] != 'uncoded':
                scheme_metrics[s['label']] = {'bler': bler, 'rate': s['real_rate'], 'type': s['type']}
            
            # Logging
            if snr % 4 == 0 or snr == snr_range_db[-1]:
                 print(f"{snr:<5.1f} | {s['label']:<12} | {ber:<10.2e} | {bler:<10.2e} | {throughput:<8.2f} | {frames:<6}")

        # 2. Adaptive Logic
        snr_eff = snr - 0.5
        target_rate_str = ""
        
        if snr_eff < 3.0:
            target_rate_str = "1/3"
        elif snr_eff < 7.0:
            target_rate_str = "1/2"
        else:
            target_rate_str = "3/4"
            
        candidates = []
        for label, m in scheme_metrics.items():
            if target_rate_str in label:
                candidates.append((label, m['bler'], m['rate']))
        
        candidates.sort(key=lambda x: x[1])
        best_label = candidates[0][0]
        
        idx = list(snr_range_db).index(snr)
        
        best_ber = results[best_label]['ber'][idx]
        best_bler = results[best_label]['bler'][idx]
        best_thpt = results[best_label]['throughput'][idx]
        
        results['Adaptive']['ber'].append(best_ber)
        results['Adaptive']['bler'].append(best_bler)
        results['Adaptive']['throughput'].append(best_thpt)
        results['Adaptive']['mode'].append(best_label)
        
        print(f"   >> Adaptive: Selected {best_label} (Eff SNR {snr_eff:.1f}dB) -> Thpt {best_thpt:.2f}")

    return snr_range_db, results

def plot_results(snr, results):
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Common Style
    plt.rcParams.update({'font.size': 14})
    
    # ---------------------------------------------------------
    # 1. BER vs SNR for LDPC and Polar (Rayleigh Channel)
    # Filenames: proposal_ber.png, ber_plot.png, ber_realistic.png
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 7))
    plt.semilogy(snr, results['Adaptive']['ber'], 'k-o', linewidth=3, markersize=10, label='Adaptive (ACM)')
    
    # Plotting multiple rates for LDPC and Polar as requested
    for label in results:
        if 'LDPC' in label and '1/2' in label:
            plt.semilogy(snr, results[label]['ber'], 'b-s', linewidth=2, alpha=0.7, label=label)
        elif 'Polar' in label and '1/2' in label:
            plt.semilogy(snr, results[label]['ber'], 'g-d', linewidth=2, alpha=0.7, label=label)
    
    if 'Uncoded' in results:
        plt.semilogy(snr, results['Uncoded']['ber'], 'r--', linewidth=2, label='Uncoded BPSK')

    plt.title('Bit Error Rate vs. SNR for LDPC and Polar', fontsize=16, fontweight='bold')
    plt.xlabel('SNR (dB)', fontsize=14)
    plt.ylabel('Bit Error Rate (BER)', fontsize=14)
    plt.ylim(1e-5, 0.5)
    plt.grid(True, which="both", alpha=0.4)
    plt.legend(frameon=True, fontsize=10, ncol=2)
    plt.tight_layout()
    
    for fname in ['proposal_ber.png', 'ber_plot.png', 'ber_realistic.png']:
        plt.savefig(os.path.join(results_dir, fname))
    print("Generated BER comparison plots.")

    # ---------------------------------------------------------
    # 2. BER vs SNR for Adaptive Coding Scheme
    # Filename: ber_plot_adaptive.png
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 7))
    plt.semilogy(snr, results['Adaptive']['ber'], 'k-o', linewidth=3, markersize=10, label='Adaptive (ACM)')
    plt.title('Bit Error Rate vs. SNR for Adaptive Coding Scheme', fontsize=16, fontweight='bold')
    plt.xlabel('SNR (dB)', fontsize=14)
    plt.ylabel('Bit Error Rate (BER)', fontsize=14)
    plt.grid(True, which="both", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'ber_plot_adaptive.png'))
    print("Generated Adaptive BER plot.")

    # ---------------------------------------------------------
    # 3 & 4. Throughput vs SNR (Normalised & Stepwise)
    # Filenames: proposal_throughput.png, throughput_plot.png, throughput_realistic.png
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 7))
    plt.plot(snr, results['Adaptive']['throughput'], 'k-o', linewidth=3, markersize=10, label='Adaptive (ACM)')
    
    if 'LDPC R=1/2' in results:
        plt.plot(snr, results['LDPC R=1/2']['throughput'], 'b-s', linewidth=2, alpha=0.8, label='Fixed LDPC (R=1/2)')
    if 'Polar R=1/2' in results:
        plt.plot(snr, results['Polar R=1/2']['throughput'], 'g-d', linewidth=2, alpha=0.8, label='Fixed Polar (R=1/2)')
    if 'Uncoded' in results:
        plt.plot(snr, [1.0]*len(snr), 'r--', linewidth=2, label='Uncoded (Rate=1.0)')

    plt.title('Throughput vs. SNR (Normalized & Stepwise)', fontsize=16, fontweight='bold')
    plt.xlabel('SNR (dB)', fontsize=14)
    plt.ylabel('Throughput (bits/symbol)', fontsize=14)
    plt.grid(True, alpha=0.4)
    plt.legend(frameon=True, fontsize=12, loc='lower right')
    plt.tight_layout()
    
    for fname in ['proposal_throughput.png', 'throughput_plot.png', 'throughput_realistic.png']:
        plt.savefig(os.path.join(results_dir, fname))
    print("Generated Throughput comparison plots.")

    # ---------------------------------------------------------
    # 5. BLER vs SNR for Multi-Rate LDPC and Polar
    # Filename: bler_realistic.png
    # ---------------------------------------------------------
    plt.figure(figsize=(10, 7))
    plt.semilogy(snr, results['Adaptive']['bler'], 'k-o', linewidth=3, markersize=10, label='Adaptive (ACM)')
    
    # Show more rates for BLER as requested
    for label in results:
        if ('LDPC' in label or 'Polar' in label) and ('1/3' in label or '1/2' in label or '3/4' in label):
            plt.semilogy(snr, results[label]['bler'], alpha=0.6, label=label)
    
    plt.title('BLER vs. SNR for Multi-Rate LDPC and Polar', fontsize=16, fontweight='bold')
    plt.xlabel('SNR (dB)', fontsize=14)
    plt.ylabel('Block Error Rate (BLER)', fontsize=14)
    plt.grid(True, which="both", alpha=0.4)
    plt.legend(ncol=2, fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'bler_realistic.png'))
    print("Generated Multi-Rate BLER plot.")


if __name__ == "__main__":
    start = time.time()
    snr, results = get_simulation_results()
    plot_results(snr, results)
    print(f"Total Time: {time.time()-start:.1f}s")
