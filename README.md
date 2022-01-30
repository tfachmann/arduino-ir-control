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

#### Simple Tests

```
python scripts/watcher.py --info=DEBUG
```

#### As Systemd Unit

##### Create a unit file (`/etc/systemd/system/arduino_ir_watcher.service`) 

```
[Unit]
Description=Serial port watcher to execute commands based on ir commands
After=network.target

[Service]
Type=simple
ExecStart=<path-to/arduino-ir-control/scripts/watcher.py> --systemd
Restart=always
RestartSec=15s

[Install]
WantedBy=multi-user.target
```

##### Enable

```
sudo systemctl enable arduino_ir_watcher.service
```

On the next restart, the script will be executed.

---

To test it right away, follow the next steps.

##### Start

```
sudo systemctl daemon-reload
sudo systemctl start arduino_ir_watcher.service
```

##### Debug 

```
journalctl -b -u arduino_ir_watcher
```

Note: it might not find packages like `pyserial` if you have installed it *locally*, as this script is now executed by the user *root*, make sure `pyserial` and `systemd-python` are installed system-wide or use a virtual environment.
