import bluetooth
import time
from time import sleep

quit = False #flag variable for quitting loop
while not quit: #looped in case of connection failure
    serverMACAddress = "B8:27:EB:80:DB:D1"
    port = 3
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    try: #successfully connected
        s.connect((serverMACAddress, port))
        while True:
            print("=====First digit=====")
            print("1: room 1")
            print("2: room 2")
            print("3: room 3")
            print("=====Second digit====")
            print("0: Off")
            print("1: On")
            print("=====================")
            text = input("INPUT: ")
            if text == "quit":
                s.send('q')
                quit = True
                break
            now = time.localtime()
            stamp = "%04d%02d%02d%02d%02d%02d" % (now.tm_year,
                                                  now.tm_mon,
                                                  now.tm_mday,
                                                  now.tm_hour,
                                                  now.tm_min,
                                                  now.tm_sec)
            text = text + stamp
            s.send(text)
    except: #connection failed: retry connection
        print("Edge not found")
        print("Reconnecting in 5...")
        sleep(1)
        print("4...")
        sleep(1)
        print("3...")
        sleep(1)
        print("2...")
        sleep(1)
        print("1...")
        sleep(1)

s.close()
