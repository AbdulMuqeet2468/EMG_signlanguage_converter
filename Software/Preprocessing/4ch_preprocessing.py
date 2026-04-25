import pandas as pd
import numpy as np
from scipy.signal import filtfilt, iirnotch, cheby2

# -------- PARAMETERS --------
fs = 500  # sampling frequency (change if needed)

INPUT_FILE = "emg_5gestures_4ch.csv"
OUTPUT_FILE = "preprocessed.csv"

CHANNELS = ["ch1", "ch2", "ch3", "ch4"]

# -------- LOAD DATA --------
df = pd.read_csv(INPUT_FILE)

# -------- PROCESS EACH CHANNEL --------
for ch in CHANNELS:
    raw = df[ch].values.astype(float)

    # 1. DC removal
    dc_removed = raw - np.mean(raw)

    # 2. Notch filter (50 Hz)
    wo = 50 / (fs / 2)
    bw = wo / 35
    b_notch, a_notch = iirnotch(wo, bw)
    after_notch = filtfilt(b_notch, a_notch, dc_removed)

    # 3. Chebyshev Type II Bandpass (20–90 Hz)
    low_cut = 20
    high_cut = 90
    Wn = [low_cut / (fs / 2), high_cut / (fs / 2)]
    order = 4

    b_ch2, a_ch2 = cheby2(order, 40, Wn, btype='bandpass')
    sig_ch2 = filtfilt(b_ch2, a_ch2, after_notch)

    # 4. Smoothing (moving average)
    sm_win = int(0.1 * fs)  # 0.1 sec window
    smoothed = np.convolve(sig_ch2, np.ones(sm_win)/sm_win, mode='same')

    # Save processed channel
    df[ch + "_proc"] = smoothed

# -------- SAVE --------
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Preprocessing complete!")
print(f"📁 Saved as: {OUTPUT_FILE}")
