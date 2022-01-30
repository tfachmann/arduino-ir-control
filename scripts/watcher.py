#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
import subprocess
import sys
import time

import serial

bytes_dict = {
    b"F00FFF00": "up",
    b"F609FF00": "volume_up",
    b"E31CFF00": "down",
    b"E21DFF00": "volume_down",
    b"E817FF00": 10,
    b"ED12FF00": 20,
    b"E916FF00": 30,
    b"BF40FF00": 40,
    b"B34CFF00": 50,
    b"FB04FF00": 60,
    b"F50AFF00": 70,
    b"E11EFF00": 80,
    b"F10EFF00": 90,
    b"EB14FF00": 100,
}
delta = 1

log = logging.getLogger("watcher.py")
log.setLevel(logging.INFO)


class SerialWatcher:
    def __init__(self, device="/dev/ttyACM0", baud=9600) -> None:
        self.wait = 10
        self.device = device
        self.baud = baud
        self.cur_brightness = 30
        self.init_serial()

    def init_serial(self):
        while True:
            try:
                self.ser = serial.Serial(self.device, self.baud)
                log.info(f"Successfully initialized Serial device {self.device} with {self.baud} baud")
                return

            except serial.SerialException:
                log.info(f"Could not allocate Serial port, retrying in {self.wait} seconds...")
                time.sleep(self.wait)
                continue

    def run(self):
        while True:
            data = self.ser.readline()

            for known_bytes in bytes_dict.keys():
                if not known_bytes in data:
                    continue
                decoded = bytes_dict[known_bytes]
                log.info(f"Received: {data} => {decoded}")
                if type(decoded) == int:
                    subprocess.call(["/usr/local/bin/brightness_monitor_external", str(decoded)])
                    self.cur_brightness = decoded
                elif decoded == "up":
                    self.cur_brightness += delta
                    subprocess.call(["/usr/local/bin/brightness_monitor_external", str(self.cur_brightness)])
                elif decoded == "down":
                    self.cur_brightness -= delta
                    subprocess.call(["/usr/local/bin/brightness_monitor_external", str(self.cur_brightness)])
                elif decoded == "volume_up":
                    subprocess.call(["lmc", "up", "5"])
                    subprocess.call(["play", "-q", "-n", "synth", "0.1", "sin", "600"])
                elif decoded == "volume_down":
                    subprocess.call(["lmc", "down", "5"])
                    subprocess.call(["play", "-q", "-n", "synth", "0.1", "sin", "400"])
            else:
                log.debug(f"Received unknown: {data}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serial port watcher")
    parser.add_argument("--log", dest="loglevel", default="INFO", type=str)
    parser.add_argument("--systemd", action="store_true")
    args = parser.parse_args()

    log.setLevel(getattr(logging, args.loglevel.upper()))

    if args.systemd:
        import systemd.journal

        handler = systemd.journal.JournalHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
        log.addHandler(systemd.journal.JournalHandler())
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        log.addHandler(handler)

    watcher = SerialWatcher()
    watcher.run()
