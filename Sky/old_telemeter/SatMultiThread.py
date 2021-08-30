import threading
import SatServerRemote

if __name__ == '__main__':
    thread1 = threading.Thread(target=SatServerRemote.SatServerRemoteRun, args=())
    thread1.start()
    while 1:
        pass
