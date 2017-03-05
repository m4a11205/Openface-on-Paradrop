import socket
import time
from optparse import OptionParser,OptionGroup

import sys, math, os, string, time, argparse, json, subprocess
import httplib
import base64
import StringIO
import thread
from flask import Flask
from flask import request

'''
Flask web interface
'''

def create_LED_App(bulb):
    app = Flask(__name__)


    @app.route('/led/on')
    def turnLedOn():
        bulb.turnOn()
        return "LED On"

    @app.route('/led/off')
    def turnLedOff():
        bulb.turnOff()
        return "LED Off"

    @app.route('/json', methods=['GET', 'POST'])
    def parseJSON():
        if request.method == 'POST':
            feature = request.form['feature']
            if(feature == "power"):
                val = request.form['value']
                if(val == "0"):
                    bulb.turnOff()
                    print("Led Off")
                elif(val == "1"):
                    bulb.turnOn()
                    print("Led On")
                else:
                    print("Error")

            elif(feature == "color"):
                r = request.form['r']
                g = request.form['g']
                b = request.form['b']
                bulb.setRgb(int(r), int(g), int(b))

            elif(feature == "brightness"):
                val = request.form['value']
                bulb.setWarmWhite(int(val))

            return ("Set LED")
        else:
            return ("error")

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app


def run_LED_App(bulb):
    app = create_LED_App(bulb)
    app.run(host = '0.0.0.0', port = 8012)


'''
LED Control Function
'''

class BulbScanner():
    def __init__(self):
        self.found_bulbs = []

    def getBulbInfoByID(self, id):
        bulb_info = None
        for b in self.found_bulbs:
            if b['id'] == id:
                return b
        return b

    def getBulbInfo(self):
        return self.found_bulbs

    def scan(self, timeout=10):

        DISCOVERY_PORT = 48899

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', DISCOVERY_PORT))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        msg = "HF-A11ASSISTHREAD"

        # set the time at which we will quit the search
        quit_time = time.time() + timeout

        response_list = []
        # outer loop for query send
        while True:
            if time.time() > quit_time:
                break
            # send out a broadcast query
            sock.sendto(msg, ('<broadcast>', DISCOVERY_PORT))

            # inner loop waiting for responses
            while True:

                sock.settimeout(1)
                try:
                    data, addr = sock.recvfrom(64)
                except socket.timeout:
                    data = None
                    if time.time() > quit_time:
                        break

                if data is not None and data != msg:
                    # tuples of IDs and IP addresses
                    item = dict()
                    item['ipaddr'] = data.split(',')[0]
                    item['id'] = data.split(',')[1]
                    item['model'] = data.split(',')[2]
                    response_list.append(item)

        self.found_bulbs = response_list
        return response_list


def percentToByte(percent):
	if percent > 100:
		percent = 100
	if percent < 0:
		percent = 0
	return int((percent * 255)/100)


def scan():
    # my code here
    scanner = BulbScanner()
    scanner.scan(timeout=2)
    bulb_info_list = scanner.getBulbInfo()
    # we have a list of buld info dicts
    addrs = []
    if len(bulb_info_list) > 0:
        for b in bulb_info_list:
            addrs.append(b['ipaddr'])
    else:
        print
        "{} bulbs found".format(len(bulb_info_list))
        for b in bulb_info_list:
            print
            "  {} {}".format(b['id'], b['ipaddr'])
        #sys.exit(0)
    return addrs

class WifiLedBulb():
    def __init__(self, ipaddr, port=5577):
        self.ipaddr = ipaddr
        self.port = port
        self.__is_on = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ipaddr, self.port))
        self.__state_str = ""

    def __str__(self):
        return self.__state_str


    def turnOn(self, on=True):
        if on:
            msg = bytearray([0x71, 0x23, 0x0f])
        else:
            msg = bytearray([0x71, 0x24, 0x0f])

        self.__write(msg)
        self.__is_on = on

    def isOn(self):
        return self.__is_on

    def turnOff(self):
        self.turnOn(False)

    def setRgb(self, r, g, b, persist=True):
        if persist:
            msg = bytearray([0x31])
        else:
            msg = bytearray([0x41])
        msg.append(r)
        msg.append(g)
        msg.append(b)
        msg.append(0x00)
        msg.append(0xf0)
        msg.append(0x0f)
        self.__write(msg)

    def setWarmWhite(self, level, persist=True):
        if persist:
            msg = bytearray([0x31])
        else:
            msg = bytearray([0x41])
        msg.append(0x00)
        msg.append(0x00)
        msg.append(0x00)
        msg.append(percentToByte(level))
        msg.append(0x0f)
        msg.append(0x0f)
        self.__write(msg)

    def __writeRaw(self, bytes):
        self.socket.send(bytes)

    def __write(self, bytes):
        # calculate checksum of byte array and add to end
        csum = sum(bytes) & 0xFF
        bytes.append(csum)
        # print "-------------",utils.dump_bytes(bytes)
        self.__writeRaw(bytes)


def parseArgs():
    parser = OptionParser()
    power_group = OptionGroup(parser, 'Power options (mutually exclusive)')
    mode_group = OptionGroup(parser, 'Mode options (mutually exclusive)')
    other_group = OptionGroup(parser, 'Other options')

    parser.add_option("-s", "--scan",
                      action="store_true", dest="scan", default=False,
                      help="Search for bulbs on local network")
    power_group.add_option("-1", "--on",
                           action="store_true", dest="on", default=False,
                           help="Turn on specified bulb(s)")
    power_group.add_option("-0", "--off",
                           action="store_true", dest="off", default=False,
                           help="Turn off specified bulb(s)")
    parser.add_option_group(power_group)

    mode_group.add_option("-c", "--color", dest="color", default=None,
                          help="Set single color mode.  Can be either color name, web hex, or comma-separated RGB triple",
                          metavar='COLOR')
    parser.add_option_group(mode_group)

    other_group.add_option("-v", "--volatile",
                           action="store_true", dest="volatile", default=False,
                           help="Don't persist mode setting with hard power cycle (RGB and WW modes only).")
    parser.add_option_group(other_group)

    (options, args) = parser.parse_args()
    return (options, args)


'''
Main
'''

if __name__ == "__main__":
    (options, args) = parseArgs()
    addrs = []
    bulb_ip = ""
    bulb    = None

    print("In LED Control Main")

    '''
    ## connect the LED bulb
    while(bulb_ip == ""):
        print('Start scanning the network to connet WifiLED')
        rst = scan()
        print('End scan')

        if (len(rst) > 0):
            bulb_ip = rst[0]
        else:
            time.sleep(2)
            continue

        print("LED ip: ", bulb_ip)
        bulb = WifiLedBulb(bulb_ip)
        bulb.setRgb(100, 0, 100)
    '''

    bulb_ip = "192.168.128.187"
    bulb = WifiLedBulb(bulb_ip)
    bulb.setRgb(100, 0, 100)

    ## start multi-thread to listening the flask packet
    try:
       thread.start_new_thread( run_LED_App, (bulb,) )
    except:
       print "Error: unable to start thread in LED control"

    while(True):
        continue

'''
    if options.scan:
        scan()
    else:
        addrs = args
        for addr in args:
            bulb = WifiLedBulb(addr)
    if options.on:
        bulb.turnOn()
    elif options.off:
        bulb.turnOff()
    if options.color is not None:
        bulb.setRgb(options.color[0], options.color[1], options.color[2])
'''
