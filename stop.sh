#!/bin/bash
# Stop pulseaudio loopback
pactl unload-module module-loopback

# Kill Python script
pkill -f recorder.py
