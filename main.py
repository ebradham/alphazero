#
# AlphaZero
#
# This code is open-source. Feel free to modify and redistribute as you want.
#
#
# a python e-typewriter using eink and a USB keyboard
# this program outputs directly to the SPI eink screen, and is driven by a
# raspberry pi zero 2w. 
#
# I programmed to work with the 7in5_V2 from Waveshare, but it should be able to work with any size display with a few minor changes.
#

from AlphaZero import alphaZero
import RPi.GPIO as GPIO
from subprocess import call
from keyboard import hook
from keyboard import wait
from time import sleep
from threading import Thread

def key_reader():
    def process_key(e):
        global key_queue
        global shift
        global ctrl
        global alt
        global filename
        global backspace
        if (e.scan_code <= 52 and e.scan_code != 1) or e.scan_code in [56, 57, 100]:
            if e.name == 'backspace':
                if e.event_type == 'down':
                    if not backspace:
                        backspace = not backspace
                        if key_queue:
                            key_queue = key_queue[:-1]
                        else:
                            alphazero.process_backspace()
                else:
                    backspace = not backspace
            elif e.name == 'ctrl':
                ctrl = not ctrl
            elif e.name == 'alt':
                if (not alt and e.event_type == 'down') or e.event_type == 'up':
                    alt = not alt 
            else:
                if ctrl and e.event_type == 'up':
                    # if e.name == 'o':
                        # print('view documents to open')
                        # options = alphazero.get_documents()
                        # while True:
                            # x = input()
                            # y = ord(x) - 97
                            # if y >= 0 and y < len(options):
                                # alphazero.open_document(options[y])
                                # key_queue = ""
                                # break
                    if e.name == 's':
                        print('saving')
                        alphazero.save_document()
                        key_queue = ""
                    elif e.name == 'n':
                        print('saving')
                        alphazero.save_document()
                        print('new document')
                        key_queue = ""
                        alphazero.new_document()
                elif ((e.name == 'shift' and e.event_type == 'down' and not shift) or (e.name == 'shift' and e.event_type == 'up')):
                    shift = not shift
                elif e.event_type == 'down' and e.name != 'shift' and e.name != 'ctrl' and not ctrl:
                    if shift:
                        e.name = e.name.upper()
                    if e.name == 'space':
                        e.name = ' '
                    elif alt:
                        e.name = alt_key(e)
                    elif e.name == 'tab':
                        e.name = '    '
                    
                    key_queue += e.name
                    print(e.name + " " + str(e.scan_code) + " " + e.event_type)
 
            

    def alt_key(e):
        return key_dict.get(e.scan_code, e.name)
        
    key_dict = {
        1: '~',
        15: '!',
        30: '@',
        31: '#',
        32: '$',
        33: '%',
        34: '^',
        35: '&',
        36: '*',
        37: '(',
        38: ')',
        39: '_',
        48: '"',
        49: '?',
        50: '{',
        51: '}',
        52: '|',
        28: '+'
    }
    hook(process_key)
    wait()



def update_screen():
    global key_queue
    while True:
        sleep(.25)
        if key_queue and not key_queue.isspace(): 
            kq = key_queue
            key_queue = ""
            alphazero.update_document(kq)

def power_down():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.wait_for_edge(3, GPIO.FALLING)
    alphazero.sleep()
    call(['shutdown', '-h', 'now'], shell=False)

alphazero = alphaZero()
key_queue = ""


shift = False
ctrl = False
backspace = False
alt = False
keyboard_listener_thread = Thread(target=key_reader)
display_update_thread = Thread(target=update_screen)
power_button_thread = Thread(target=power_down)

print('start')
keyboard_listener_thread.start()
display_update_thread.start()
power_button_thread.start()
