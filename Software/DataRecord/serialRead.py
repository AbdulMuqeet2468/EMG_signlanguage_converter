import serial
import csv
import time

PORT = '/dev/cu.SLAB_USBtoUART'   # change if needed
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

RELAX_TIME = 4
CONTRACT_TIME = 4
CYCLES = 5

FILE_NAME = "emg_dataset.csv"

print("Get ready...")

with open(FILE_NAME, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "ch1", "label"])

    for cycle in range(CYCLES):
        print(f"\nCycle {cycle+1}/{CYCLES}")

        # ---------- RELAX ----------
        print(">>> RELAX (4 sec)")
        start = time.time()

        while time.time() - start < RELAX_TIME:
            elapsed = time.time() - start

            line = ser.readline().decode(errors='ignore').strip()
            if line:
                try:
                    t, val = line.split(",")

                    # record only between 1s and 3s
                    if 1 < elapsed < 3:
                        writer.writerow([t, val, "RELAX"])

                except:
                    pass

        # ---------- CONTRACT ----------
        print(">>> CONTRACT (4 sec)")
        start = time.time()

        while time.time() - start < CONTRACT_TIME:
            elapsed = time.time() - start

            line = ser.readline().decode(errors='ignore').strip()
            if line:
                try:
                    t, val = line.split(",")

                    # record only between 1s and 3s
                    if 1 < elapsed < 3:
                        writer.writerow([t, val, "CONTRACT"])

                except:
                    pass

print("\nDone!")
print(f"Saved as: {FILE_NAME}")
