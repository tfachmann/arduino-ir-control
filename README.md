# Arduino IR Control

I use this script to change the brightness of my external monitor through an IR remote.
This simple project is not programmed in a general fashion and consists of two parts.

## Arduino IR Receiver

All the build files as well as `main.cpp` is targeted for the IR receiving end, in this case an Arduino UNO.

### Requirements

Even though it is a complete overkill, this project uses the [Arduino-CMake-Toolchain](https://github.com/a9183756-gh/Arduino-CMake-Toolchain/) for deployment.
Alternative options are collected [here](https://wiki.archlinux.org/title/Arduino).

### Build and Deployment
```sh
mkdir build
cmake -D CMAKE_TOOLCHAIN_FILE=/<path-to>/Arduino-CMake-Toolchain/Arduino-toolchain.cmake -D ARDUINO_BOARD_OPTIONS_FILE=/<path-to>/arduino-ir-control/BoardOptions.cmake ..
make SERIAL_PORT=/dev/ttyACM0 upload-arduino_ir_control
```

---

## Python Watcher

This python watcher located in `script/watcher.py` is not meant to be general, but will give you an idea how to read from the Serial port and match the bytes 

### Usage

```
python scripts/watcher.py
```

