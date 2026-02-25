# Transmission Line Fault Analysis & Parameter Estimation

This repository contains a Python-based framework for analyzing power system fault data. It utilizes two distinct mathematical approaches—**Discrete Fourier Transform (DFT)** and the **Differential Equation Algorithm**—to determine line impedance and characterize fault behavior.

##  Project Overview
When a fault occurs on a transmission line, protective relays must quickly calculate the impedance to the fault to decide whether to trip the circuit. This project demonstrates:
1. **Waveform Visualization:** Synchronized plotting of Voltage and Current.
2. **Frequency Domain Analysis:** Using DFT to extract fundamental phasors and identify DC offset components.
3. **Time-Domain Estimation:** Using the Differential Equation method to solve for physical Resistance ($R$) and Inductance ($L$) while ignoring transient distortions.



##  Mathematical Methods

### 1. Discrete Fourier Transform (DFT)
The script performs a DFT on a full-cycle window (36 samples at 60Hz).
- **Phasor Extraction:** Extracts the magnitude and phase of the 60Hz fundamental.
- **DC Offset Detection:** Analyzes the "Bin 0" component of the spectrum, which represents the decaying DC transient often seen in fault currents.
- **Phasor Diagrams:** Automatically generates polar plots to visualize the phase relationship ($\theta$) between voltage and current.



### 2. Differential Equation Algorithm (Trapezoidal Rule)
To calculate $R$ and $L$ directly without being affected by DC offset, the script solves the lumped-parameter line model:
$$v(t) = R \cdot i(t) + L \frac{di(t)}{dt}$$

Using the **Trapezoidal Rule**, the differential equation is discretized as:
$$\frac{v_k + v_{k+1}}{2} = R \left( \frac{i_k + i_{k+1}}{2} \right) + L \left( \frac{i_{k+1} - i_k}{\Delta t} \right)$$

The script uses a **Least Squares (LSTSQ)** solver to process all 36 samples simultaneously, providing a robust estimate that averages out measurement noise.



##  File Structure
- `estimate_impedance.py`: The main analysis script.
- `For Proj 1.xlsx`: Input data file containing Time, Voltage, and Current columns.
- `Combined_Waveform.png`: Exported plot showing the relationship between V and I.
- `Fault_Window_XXX_XXX.png`: Spectral analysis and phasor diagrams for specific fault windows.

##  How to Run
1. Ensure you have the required libraries installed:
   ```bash
   pip install pandas numpy matplotlib openpyxl
