import time, os
from PyUserInput.pymouse import PyMouse
from PyUserInput.pykeyboard import PyKeyboard
import _thread as thread

m = PyMouse()
k = PyKeyboard()

def mouseAkey():
    time.sleep(2)
    k.type_string('+a')
    time.sleep(1)
    k.tap_key(k.enter_key)
    time.sleep(1)
    k.type_string('sip:1000@10.112.244.60')
    time.sleep(1)
    k.tap_key(k.enter_key)
    time.sleep(1) 
    k.type_string('sip:10.112.244.60')
    time.sleep(1)
    k.tap_key(k.enter_key) 
    time.sleep(1)
    k.type_string('*')
    time.sleep(1)
    k.tap_key(k.enter_key) 
    time.sleep(1)
    k.type_string('1000')
    time.sleep(1)
    k.tap_key(k.enter_key) 
    time.sleep(1)
    k.type_string('1000')
    time.sleep(1)
    k.tap_key(k.enter_key) 

    time.sleep(3)
    k.tap_key(k.enter_key)
    time.sleep(1)
    #k.tap_key(k.enter_key)
    #k.tap_key(k.enter_key)
    k.type_string('m')
    time.sleep(1)
    k.tap_key(k.enter_key)
    time.sleep(1)
    k.type_string('sip:2000@10.112.244.60')
    time.sleep(1)
    k.tap_key(k.enter_key)

if __name__ == "__main__":
    thread.start_new_thread(mouseAkey, ())
    # os.system(r"/home/ubuntu/Desktop/pjsip/pjsip/pjproject-2.6/pjsip-apps/bin/pjsua-x86_64-unknown-linux-gnu")
    os.system(r"F:\VirtualStudioProgram\pjproject-wyh\pjsip-apps\bin\pjsua-i386-Win32-vc14-Debug.exe")


