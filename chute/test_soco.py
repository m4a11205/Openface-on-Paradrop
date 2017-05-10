import socket
import time
import sys, math, os, string, time, argparse, json, subprocess
import httplib
import base64
import StringIO
import thread
from flask import Flask
from flask import request
from soco import SoCo


URL_BASE = {'ted': 'http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3',
'sean': 'http://fmn.rrimg.com/fmn059/audio/20140822/0210/m_mTCE_490d00001683125d.mp3'}

# https://docs.google.com/uc?export=open&id=0BwZNdRbemZmsSndXUWRmOVQxaXc
ALARML_URL = 'http://gdurl.com/5lI7'
U0 = 'https://doc-10-7k-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/87d1kuv0ghqscgj1hg904467vq6bolss/1492639200000/16833314890502965928/*/0BwZNdRbemZmsVENyem8tR1ZaZ2s'

U1 = 'http://gdurl.com/5lI7'

U2 = 'http://gdurl.com/5lI7.mp3'


'''
Flask web interface
'''
def create_SONO_App(sonos):
    app = Flask(__name__)

    @app.route('/alarm')
    def alarm():
        sonos.alarm()
        return "SONO alarm"

    @app.route('/pause')
    def pause():
        sonos.pause()
        return "SONO pause"

    return app


def run_SONO_App(sonos):
    print("\n SONO Speaker Controller App is ready !!!\n")
    app = create_SONO_App(sonos)
    app.run(host = '0.0.0.0', port = 8015)


class SonoController():
    def __init__(self, ip):
        self.core = SoCo(ip)

    def play_uri(self, url):
        self.core.play_uri(url)

    def play_by_userName(self, name):
        url = URL_BASE[name]
        self.core.play_uri(url)

    def pause(self):
        self.core.pause()

    def mute(self):
        self.core.mute = True

    def unMute(self):
        self.core.mute = False

    def setVolume(self, val):
        self.core.volume = val

    def alarm(self):
        self.play_uri(ALARM_URL)
        time.sleep(8.0)
        self.pause()


def connectSpeaker():
    sono_ip = "192.168.128.181"
    sonos = SonoController(sono_ip)

    ## start multi-thread to listening the flask packet
    try:
       thread.start_new_thread( run_SONO_App, (sonos,) )
    except:
       print "Error: unable to start thread in Sonos Speaker Control"

    return sonos


if __name__ == '__main__':
    sono_ip = "192.168.128.181"
    sonos = SonoController(sono_ip)
    # You could use the discover function instead, if you don't know the IP

    # Pass in a URI to a media file to have it streamed through the Sonos
    # speaker
    #sonos.play_uri(ALARM_URL)
    sonos.play_uri(U0)
    #sonos.pause()
