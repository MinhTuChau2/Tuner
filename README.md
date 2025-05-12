# 🎸 Real-Time Guitar Tuner (Python)

A simple terminal-based real-time guitar tuner written in Python. This tuner uses your microphone to detect the pitch of a played string and gives tuning feedback based on standard tuning (E A D G B E).

## 🔧 Features

- Detects fundamental pitch using Fast Fourier Transform (FFT)
- Filters audio input to reduce noise and avoid harmonics
- Provides real-time feedback (In tune / Too sharp / Too flat)
- Works with any microphone device (selectable on launch)
- Designed for standard tuning: E2, A2, D3, G3, B3, E4

## 🎼 Tuning Frequencies

| String | Note | Frequency (Hz) |
|--------|------|----------------|
| 6      | E2   | 82.41          |
| 5      | A2   | 110.00         |
| 4      | D3   | 146.83         |
| 3      | G3   | 196.00         |
| 2      | B3   | 246.94         |
| 1      | E4   | 329.63         |

## 🧪 Requirements

- Python 3.7+
- [sounddevice](https://python-sounddevice.readthedocs.io/)
- numpy
- scipy
