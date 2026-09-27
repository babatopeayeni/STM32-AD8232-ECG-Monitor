import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# -----------------------------
# Serial settings
# -----------------------------
PORT = "COM5"
BAUD_RATE = 115200

# Number of ADC samples displayed
WINDOW_SIZE = 500

# Open STM32 serial connection
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

# Storage for incoming ADC samples
data = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

# Create graph
fig, ax = plt.subplots()
line, = ax.plot(range(WINDOW_SIZE), data)

ax.set_title("STM32 AD8232 ECG Monitor")
ax.set_xlabel("Samples")
ax.set_ylabel("ADC Value")

# STM32 12-bit ADC range
ax.set_ylim(0, 4095)
ax.set_xlim(0, WINDOW_SIZE - 1)

def update(frame):
    # Read several available samples each update
    while ser.in_waiting:
        try:
            raw = ser.readline().decode("utf-8").strip()

            if raw:
                adc_value = int(raw)

                if 0 <= adc_value <= 4095:
                    data.append(adc_value)

        except (ValueError, UnicodeDecodeError):
            pass

    line.set_ydata(data)
    return line,

ani = FuncAnimation(
    fig,
    update,
    interval=20,
    blit=True,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()

ser.close()