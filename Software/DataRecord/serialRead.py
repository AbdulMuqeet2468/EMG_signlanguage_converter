import serial
import csv
import time

PORT = '/dev/cu.SLAB_USBtoUART'
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)

GESTURES = [
    "FIST",
    "OPEN",
    "FLEXION",
    "EXTENSION",
    "PINCH"
]

GESTURE_TIME = 4
CYCLES = 5

FILE_NAME = "emg_5gestures_4ch.csv"

print("Get ready...")

with open(FILE_NAME, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "ch1", "ch2", "ch3", "ch4", "label"])

    for cycle in range(CYCLES):
        print(f"\nCycle {cycle+1}/{CYCLES}")

        for gesture in GESTURES:
            print(f">>> {gesture} (4 sec)")
            start = time.time()

            while time.time() - start < GESTURE_TIME:
                elapsed = time.time() - start

                line = ser.readline().decode(errors='ignore').strip()

                if line:
                    try:
                        # Expecting: t,ch1,ch2,ch3,ch4
                        parts = line.split(",")

                        if len(parts) == 5:
                            t, ch1, ch2, ch3, ch4 = parts

                            # keep only stable region (1s–3s)
                            if 1 < elapsed < 3:
                                writer.writerow([t, ch1, ch2, ch3, ch4, gesture])

                    except:
                        pass

print("\n✅ Done!")
print(f"📁 Saved as: {FILE_NAME}")
