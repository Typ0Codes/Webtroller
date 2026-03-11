# Webtroller

turn your webcam into a controller

[![Webtroller Testing](https://img.youtube.com/vi/0mBjVbauqRY/0.jpg)](https://www.youtube.com/watch?v=0mBjVbauqRY)   

## Install

### Dependencies:
OpenCV \
Mediapipe \
Vgamepad 

```
//install dependencies
pip install opencv-python mediapipe vgamepad
```

### Windows install

download this repo

install the depenedencies by running

```
pip install opencv-python mediapipe vgamepad
```

in the terminal

then open the folder containing the repo in the termninal and run

```python3 webtroller.py```

### Linux install

download this repo

follow this [Guide](https://github.com/yannbouteiller/vgamepad/blob/main/readme/linux.md) to install vgamepad

install the other dependencies 

then open the folder containing the repo in the termninal and run

```python3 webtroller.py```

## Usage

run

```python3 webtroller.py```

in the folder containing this repo

To press a button close your fist \
a fist is defined as when your fingers are below your wrist

The large green dot is the hitbox for pressing buttons. it needs to be inside the button for it to press.

## Potential future features

- Window resizing
- Custom button placements
- Less cumbersome to launch
- Remove opencv default ui at the top
- full support for the kinect 1
