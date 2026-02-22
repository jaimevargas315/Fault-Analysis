import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_excel("For Proj 1.xlsx")
Time = df["Time(s)"]
Voltage = df["Voltage(kV)"]
Current = df["Current(A)"]

# 1. Create one wide figure
fig, ax1 = plt.subplots(figsize=(15, 6))

# --- Plot Voltage on the Primary Y-Axis (Left) ---
color_v = '#000000'
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Voltage (kV)', color=color_v, fontsize=12, fontweight='bold')
line1 = ax1.plot(Time, Voltage, color=color_v, label="Voltage (kV)", linewidth=1.5)
ax1.tick_params(axis='y', labelcolor=color_v)

# --- Plot Current on a Secondary Y-Axis (Right) ---
ax2 = ax1.twinx()  # This creates the shared x-axis
color_i = 'tab:red'
ax2.set_ylabel('Current (A)', color=color_i, fontsize=12, fontweight='bold')
line2 = ax2.plot(Time, Current, color=color_i, label="Current (A)", linewidth=1.5)
ax2.tick_params(axis='y', labelcolor=color_i)

# --- Formatting Ticks and Grids ---
start_time, end_time = Time.min(), Time.max()
ax1.set_xticks(np.arange(start_time, end_time, step=0.01))
ax1.minorticks_on()

# Grid usually looks best on the primary axis only to avoid "checkerboard" overlap
ax1.grid(which='major', linestyle='-', linewidth='0.5', color='black', alpha=0.3)
ax1.grid(which='minor', linestyle=':', linewidth='0.5', color='gray', alpha=0.3)

# --- Merging the Legends ---
# Since we have two axes, we combine the legend handles into one box
lns = line1 + line2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper right')

plt.title("Combined Voltage and Current Waveform", fontsize=14)
fig.tight_layout()
plt.savefig("Combined_Waveform.png", dpi=300)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
def analyze_fault_window(start_idx):
    """
    Performs DFT and Phasor analysis on a 36-sample window 
    starting at start_idx.
    """
    N = 36
    Fs = 2160
    end_idx = start_idx + N
    
    # 1. Slice the data
    v_cycle = Voltage.iloc[start_idx:end_idx].to_numpy()
    i_cycle = Current.iloc[start_idx:end_idx].to_numpy()
    
    # 2. Perform DFT
    V_dft = np.fft.fft(v_cycle)
    I_dft = np.fft.fft(i_cycle)
    
    # 3. Calculate RMS and Phases
    V_fund_rms = (np.sqrt(2) / N) * np.abs(V_dft[1])
    I_fund_rms = (np.sqrt(2) / N) * np.abs(I_dft[1])
    V_phase = np.degrees(np.angle(V_dft[1]))
    I_phase = np.degrees(np.angle(I_dft[1]))
    theta = V_phase - I_phase
    
    # DC Components (Bin 0)
    V_dc = (1/N) * np.abs(V_dft[0])
    I_dc = (1/N) * np.abs(I_dft[0])

    # 4. Frequency Spectrum Setup
    freqs = np.fft.fftfreq(N, 1/Fs)
    pos_freqs = freqs[:N//2]
    V_rms_spec = (np.sqrt(2) / N) * np.abs(V_dft[:N//2])
    V_rms_spec[0] = V_dc # Fix DC scaling for plot
    I_rms_spec = (np.sqrt(2) / N) * np.abs(I_dft[:N//2])
    I_rms_spec[0] = I_dc

    # --- PLOTTING ---
    fig = plt.figure(figsize=(15, 6))
    
    # Subplot 1: Voltage Spectrum (Shows V_dc)
    ax_v_spec = plt.subplot(131)
    ax_v_spec.stem(pos_freqs, V_rms_spec[:N//2], 'b')
    ax_v_spec.set_title(f"Voltage RMS Spectrum (Samples {start_idx+1}-{end_idx})")
    ax_v_spec.set_xlabel("Hz")
    ax_v_spec.set_ylabel("kV (RMS)")

    # Subplot 2: Frequency Spectrum
    ax_spec = plt.subplot(132)
    ax_spec.stem(pos_freqs, I_rms_spec[:N//2], 'r', label='Current')
    ax_spec.set_title(f"Current RMS Spectrum (Samples {start_idx+1}-{end_idx})")
    ax_spec.set_xlabel("Hz")
    ax_spec.set_ylabel("Amps (RMS)")

    # Subplot 3: Phasor Diagram
    ax_polar = plt.subplot(133, projection='polar')
    v_rad = np.radians(V_phase)
    i_rad = np.radians(I_phase)
    
    # Normalized arrows (length = 1.0)
    ax_polar.annotate('', xy=(v_rad, 1.0), xytext=(0, 0),
                arrowprops=dict(edgecolor='black', facecolor='black', arrowstyle='->', lw=3))
    ax_polar.annotate('', xy=(i_rad, 1.0), xytext=(0, 0),
                arrowprops=dict(edgecolor='red', facecolor='red', arrowstyle='->', lw=3))
    
    # Labels with rounded decimals
    ax_polar.text(v_rad, 1.25, f'V: {V_fund_rms:.2f} kV\n{V_phase:.2f}°', color='black', fontweight='bold', ha='center')
    ax_polar.text(i_rad, 1.25, f'I: {I_fund_rms:.2f} A\n{I_phase:.2f}°', color='red', fontweight='bold', ha='center')
    ax_polar.text(np.radians(I_phase + theta/2), 0.5, f'θ= {theta:.2f}°', color='purple', fontweight='bold')
    
    ax_polar.set_title(f"Phasor Diagram\nDC Offset: {I_dc:.2f} A", va='bottom', fontweight='bold')
    ax_polar.set_yticklabels([]) 
    ax_polar.set_rmax(1.5) # Space for labels
    
    plt.tight_layout()
    plt.savefig(f"Fault_Window_{start_idx+1}_{end_idx}.png", dpi=300)
    plt.show()

# --- CALL THE FUNCTION ---

# Check the START of the fault
analyze_fault_window(0)

# Check the END of the fault (301-336)
analyze_fault_window(300)

