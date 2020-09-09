# Osu-Key-Masher
Show a cute animation of what key you are pressing when playing OSU!

* Windows only! The transparency effect is achieved using the Win32 APIs, a linux version is in the works!


## Setup
Install `pygame`, `pynput` and `pywin32` with pip.
```
pip install pygame pynput pywin32
```

## Run
Run `osu_key_masher.py`

## Configuration
The configuration file `config.cfg` allows for a decent amount of configuration without modifying the source code:
```
[PROGRAM]
resolution_x = 1280 # size of the window  
resolution_y = 720
transparency_rgb = #0A0A0A # colour for transparency chroma key (might be visible)
target_framerate = 200  # target framerate for animation

[KEYS]
left=z # set the key you use for left in osu
right=x # and right
```
