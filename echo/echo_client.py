#! /usr/bin/env python

import sys
import socket
import requests
import threading


UDP_IP = '127.0.0.1'
UDP_PORT = 9898
REQUEST_DATA = {'ip': UDP_IP, 'port': UDP_PORT}
REQUEST_URL = 'https://famous-vista-512.appspot.com/echo'
BUFFER_SIZE = 1024

def listen():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', UDP_PORT))
        data, addr = sock.recvfrom(BUFFER_SIZE)
        print 'from', addr, 'received:', data
    except socket.timeout:
        print 'Timed out'
    except socket.error, err:
        print err
    finally:
        sock.close()

def make_request(msg):
    try:
        data = {'ip': UDP_IP, 'port': UDP_PORT, 'msg': msg}
        response = requests.post(REQUEST_URL, data=data)
        print 'response:', response.text
    except requests.exceptions.ConnectionError:
        print 'Connection error'

def fail(err_msg):
    sys.stderr.write(err_msg + '\n')
    sys.exit(1)

def process_message(msg):
    thread = threading.Thread(target=listen)
    thread.start()
    make_request(msg)
    thread.join()

def main():
    try:
        socket.setdefaulttimeout(float(sys.argv[1]))
    except (IndexError, ValueError):
        fail('First argument must be timeout in seconds')

    try:
        while True:
            process_message(raw_input('your message: '))
    except (KeyboardInterrupt, EOFError):
        pass


if __name__ == '__main__':
    main()
