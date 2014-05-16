import serial
import sys
import time


if __name__ == '__main__':
  f = open('/tmp/blue_dev', 'r')
  dev = f.readline()
  f.close()
  s = serial.Serial(dev, 9600, timeout=5)
  while True:
    res = s.read()
    print res
    time.sleep(0.5)
