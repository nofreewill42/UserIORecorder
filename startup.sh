#!/bin/bash
# Start pulseaudio loopback with 1ms latency
pactl load-module module-loopback latency_msec=1

# Activate your Python virtual environment
#conda deactivate
#source venv/bin/activate

# Start your Python script
#python recorder_allinone.py
#python recorder_copy2.py
python recorder.py

# Stop pulseaudio loopback
pactl unload-module module-loopback
