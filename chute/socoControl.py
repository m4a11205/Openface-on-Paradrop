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
'Sean': 'http://fmn.rrimg.com/fmn059/audio/20140822/0210/m_mTCE_490d00001683125d.mp3',
'Unknown': 'Unknown'
}

MUSIC_BASE = {'http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3':'Wonderboy',
 'http://fmn.rrimg.com/fmn059/audio/20140822/0210/m_mTCE_490d00001683125d.mp3': 'm_mTCE_490d00001683125d.mp3',
 'http://soundbible.com/mp3/School_Fire_Alarm-Cullen_Card-202875844.mp3': 'School_Fire_Alarm-Cullen_Card-202875844.mp3'
}
# sound #
ALARM_URL = 'http://soundbible.com/mp3/School_Fire_Alarm-Cullen_Card-202875844.mp3'
START_URL = 'http://soundbible.com/mp3/dixie-horn_daniel-simion.mp3'
END_URL = 'http://soundbible.com/mp3/Page_Turn-Mark_DiAngelo-1304638748.mp3'
U0 = 'http://fmn.rrimg.com/fmn059/audio/20140822/0210/m_mTCE_490d00001683125d.mp3'
U1 = 'http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3'




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
        url = URL_BASE.get(name,"Unknown")
        if (url == "Unknown"):
            track = self.core.get_current_track_info()
            current_play = track['title']
            # print track['title']
            target_play = MUSIC_BASE.get(url, "Unknow")
            # print target_play
            if (current_play == target_play):
                print "unknown person"
            else:
                self.core.clear_queue()
                self.core.add_uri_to_queue(ALARM_URL)
                self.core.add_uri_to_queue(END_URL)
                self.core.play_from_queue(0, True)
        else:
            track = self.core.get_current_track_info()
            current_play = track['title']
            # print track['title']
            target_play = MUSIC_BASE.get(url, "Unknow")
            # print target_play
            if (current_play == target_play):
                print "the same person"
            else:
                self.core.clear_queue()
                self.core.add_uri_to_queue(url)
                self.core.add_uri_to_queue(END_URL)
                self.core.play_from_queue(0, True)

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
    sonos.play_uri(START_URL)
    ## start multi-thread to listening the flask packet
    try:
       thread.start_new_thread( run_SONO_App, (sonos,) )
    except:
       print "Error: unable to start thread in Sonos Speaker Control"

    return sonos


if __name__ == '__main__':
    # You could use the discover function instead, if you don't know the IP
    sono_ip = "192.168.128.181"    
    sonos = SonoController(sono_ip)
    
    sonos.play_uri(U1)

    # Pass in a URI to a media file to have it streamed through the Sonos
    # speaker
    #sonos.play_uri(ALARM_URL)

    #sonos = SoCo(sono_ip) # Pass in the IP of your Sonos speaker

    #sonos.pause()

    # Play a stopped or paused track
    #sonos.play()
    #print sonos.queue_size

#    speaker = sonos.get_speaker_info()  # get speaker info
#    print speaker['model_name']     # print speaker info
    '''
    zone_name, player_icon, uid, serial_number, software_version,
    hardware_version, model_number, model_name, display_version
    mac_address
    '''
#    sonos.seek('00:00:50') # seek spicific time to play
#    print sonos.mute   # return status of mute
#    sonos.mute = True   # mute
#    sonos.mute = False  # unmute
#    sonos.volume = 50  # set volume
