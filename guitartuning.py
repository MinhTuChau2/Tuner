import sounddevice as sd
import numpy as np
import time
from scipy.signal import butter, filtfilt

# Reference tuning frequencies for E A D G B E strings (standard tuning)
tuning_frequencies = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63
}

# Band-pass filter to focus on the expected string frequencies
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs):
    b, a = butter_bandpass(lowcut, highcut, fs)
    y = filtfilt(b, a, data)
    return y

# Detect pitch from audio
def detect_pitch(audio, fs):
    window = np.hanning(len(audio))
    audio = audio * window
    
    # Apply band-pass filter to remove unwanted frequencies
    filtered_audio = bandpass_filter(audio, 70, 400, fs)  # Filtering for guitar frequencies

    fft = np.fft.rfft(filtered_audio)
    freqs = np.fft.rfftfreq(len(filtered_audio), 1/fs)
    peak_idx = np.argmax(np.abs(fft))
    peak_freq = freqs[peak_idx]
    return peak_freq

# Record audio for a short duration
def record_audio(duration=1.5, fs=44100, device_index=None):
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64', device=device_index)
    sd.wait()
    return audio.flatten(), fs

# Find the closest string
def closest_string(freq):
    closest = min(tuning_frequencies.items(), key=lambda x: abs(x[1] - freq))
    return closest

# Select the microphone device
def select_microphone():
    print("Available microphones:")
    devices = sd.query_devices()
    input_devices = [device for device in devices if device['max_input_channels'] > 0]
    
    for idx, device in enumerate(input_devices):
        print(f"{idx}: {device['name']}")
    
    # Prompt user to select a device
    device_index = int(input("\nSelect microphone device by number: "))
    
    return input_devices[device_index]['index']

# Main tuning loop
def tuner_loop():
    print("🎸 Guitar Tuner - Play one string at a time\n")
    
    # Select microphone device
    device_index = select_microphone()

    try:
        while True:
            audio, fs = record_audio(device_index=device_index)
            freq = detect_pitch(audio, fs)
            if freq < 20:
                print("Too quiet or no input detected.\n")
                continue

            string, target_freq = closest_string(freq)
            diff = freq - target_freq
            print(f"Detected: {freq:.2f} Hz --> Closest: {string} ({target_freq} Hz)")

            if abs(diff) < 1.0:
                print("✅ In tune!\n")
            elif diff > 0:
                print("🔺 Too sharp, tune down.\n")
            else:
                print("🔻 Too flat, tune up.\n")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nTuner stopped.")

if __name__ == "__main__":
    tuner_loop()
