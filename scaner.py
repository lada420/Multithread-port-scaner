import socket
import argparse
import threading
from queue import Queue

checks = {}
TCP_TIMEOUT = 5
hostport_queue = None

def parseports(buf):
    res = []
    if "-" in buf:
        res = [int(i) for i in range( int(buf.split('-')[0]), int(buf.split('-')[1])+1)]
    else:
        res = [int(buf)]
    return res


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type = str, help = "target ip-addr")
    parser.add_argument("-p", type=str, help="set port or range with separator '-'")
    return parser

def scanport(host, port):
    sock = socket.socket()
    sock.settimeout(TCP_TIMEOUT)
    try:
        sock.connect((host,port))
        checks[target_ip + ':' + str(port)] = 'up'
    except:
        checks[target_ip + ':' + str(port)] = 'down'
    sock.close()

def runner():
    while 1:
        host, port = hostport_queue.get()
        scanport(host, port)
        hostport_queue.task_done()

if __name__ == "__main__":
    args = init_parser().parse_args()
    target_ip = args.ip
    ports = parseports(args.p)

    hostport_queue = Queue()
    for _ in range(50):
        thread = threading.Thread(target=runner)
        thread.daemon = True
        thread.start()
    for port in ports:
        hostport_queue.put((target_ip, port))

    hostport_queue.join()

    for i in checks:
        if checks[i]=='up':
            print(i, checks[i])