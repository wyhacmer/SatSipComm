import threading
import telemeter_socket
import telemeter_paramMod

if __name__ == '__main__':
    thread1 = threading.Thread(target=telemeter_paramMod.main_logic, args=())
    thread2 = threading.Thread(target=telemeter_socket.main_socket, args=())
    thread1.start()
    print("thread")
    thread2.start()
    while 1:
        pass
