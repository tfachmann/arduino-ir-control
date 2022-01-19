#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import sys
import subprocess

bytes_dict = {
    b'F00FFF00': "up",
    b'F609FF00': "up",
    b'E31CFF00': "down",
    b'E21DFF00': "down",
    b'E817FF00': 10,
    b'ED12FF00': 20,
    b'E916FF00': 30,
    b'BF40FF00': 40,
    b'B34CFF00': 50,
    b'FB04FF00': 60,
    b'F50AFF00': 70,
    b'E11EFF00': 80,
    b'F10EFF00': 90,
    b'EB14FF00': 100,
}
delta = 1


def main():
    ser = serial.Serial("/dev/ttyACM0", 9600)

    while True:
        data = ser.readline()

        for known_bytes in bytes_dict.keys():
            if not known_bytes in data:
                continue
            decoded = bytes_dict[known_bytes]
            print(decoded)
            if type(decoded) == int:
                subprocess.call(["brightness_monitor_external", str(decoded)])
                cur_brightness = decoded
            elif decoded == "up":
                cur_brightness += delta
                subprocess.call(["brightness_monitor_external", str(cur_brightness)])
            elif decoded == "down":
                cur_brightness -= delta
                subprocess.call(["brightness_monitor_external", str(cur_brightness)])
        else:
            print("---")
            print(data)


if __name__ == "__main__":
    main()
