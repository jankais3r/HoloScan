# HoloScan
Hologram viewer for LiDAR/TrueDepth scans in the PLY format

## Hardware Requirements
- iPad
- PC (only needed for the initial setup)
- [Looking Glass](https://lookingglassfactory.com) holographic display
- [USB-C Digital AV Multiport Adapter](https://www.apple.com/shop/product/MUF82AM/A/usb-c-digital-av-multiport-adapter) (other adapters might work as well, but YMMV)

## Software Requirements
### iOS
- [Pythonista](http://omz-software.com/pythonista/) app
- Internet connection required for the first run. Subsequent usage is possible offline.

### PC (only needed for the initial setup)
- [HoloPlay service](https://lookingglassfactory.com/software/holoplay-service)

## Setup
1) Connect the Looking Glass display to a PC with HoloPlay service installed and visit [https://eka.hn/calibration_test.html](https://eka.hn/calibration_test.html)
2) Copy the JSON block provided by the website and use it to replace the hardcoded calibration data on [row 47](https://github.com/jankais3r/HoloScan/blob/main/HoloScan.py#L47) of `HoloScan.py`
3) Transfer `HoloScan.py` to Pythonista and run it with a Python 3.x interpreter

Currently, the only supported file format is PLY (both ASCII and binary).


![Demo](https://github.com/jankais3r/HoloScan/blob/main/demo.gif)

See it in action [here](https://youtu.be/Jz1amOBU1CA).
