#!/bin/python3
# -*- coding: utf-8 -*-

import platform
import os
import socket
import _thread

import cstring

TCP_MAX_SIZE = 1024 * 1024 * 2


class NatData():
    def __init__(self):
        self.username = ''
        self.password = ''
        self.host = ''
        self.port = 8000
        self.public_ip = ''
        self.intranet_ip = ''
        self.serverhost = 'localhost'
        self.serverport = 9000
        self.bridgeport = 0
        self.proxyport = 0
        self.proxyhost = 'zerohost'

    def show_info(self):
        print('Username:', self.username)
        print('Your public ip:', self.public_ip)
        print('Your intranet ip:', self.intranet_ip)
        print('Server host:', self.serverhost)
        print('Data will be received from port: ', self.bridgeport)
        print('Port %d is proxyed.', self.port)
        print()
        print('Others can visit your native port %d by visit:', self.port)
        print(self.proxyhost + ':' + self.proxyport)
        print()


def command_menu():
    print('m   print this menu')
    print('g   login and start proxy')
    print('p   set the port that you want to proxy')
    print()
    print('l   list link infomation')
    print('c   clear screen')
    print()
    print('s   stop proxy')
    print('q   quit program')


#def del_request(natdata, proxy_socket):
def handle_response(proxy_socket, native_socket):

    header_end = False
    has_content_length = False
    is_chunked = False
    content_length = 0
    current_len = 0
    body_begin_index = 0

    while True:
        # receive response from native port.
        rep = native_socket.recv(TCP_MAX_SIZE)
        print('receive response from native port.')

        if not rep:
            break

        # send response to proxy server.
        proxy_socket.sendall(rep)

        # analyse http message
        if not header_end:
            x = cstring.find_substr(rep, b'Content-Length: ')
            if x == -1:
                y = cstring.find_substr(rep, b'Transfer-Encoding: chunked')
                if y != -1:
                    print('0000000 this is chunked 00000000')
                    is_chunked = True
            else:
                # get Content-Length
                i = x + len(b'Content-Length: ')
                len_str = ''
                while rep[i] != ord('\r'):
                    len_str += chr(rep[i])
                    i += 1
                content_length = int(len_str)
                has_content_length = True

            # find header end
            k = cstring.find_substr(rep, b'\r\n\r\n')
            if k != -1:
                body_begin_index = k + len(b'\r\n\r\n')
                current_len = len(rep) - body_begin_index
                header_end = True

        if has_content_length:
            current_len += len(rep)
            if current_len >= content_length:
                break
        if is_chunked:
            current_len += len(rep)
            if rep.endswith(b'0\r\n\r\n'):
                break
    proxy_socket.sendall(b'zero\r\n\r\n')
    print('**********response end**********')


def start_proxy(natdata):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((natdata.serverhost, natdata.serverport))
    s.sendall((natdata.username + ' ' + natdata.password).encode('utf-8'))
    login_result = s.recv(TCP_MAX_SIZE).decode('utf-8')
    print()
    print(login_result)
    login_result = login_result.split('\n')
    if login_result[0] == 'success':
        natdata.proxyhost = login_result[1]
        natdata.proxyport = int(login_result[2])

        # create socket s1 to connect to native port you want to proxy.
        try:
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.connect((socket.gethostname(), natdata.port))
            s.sendall(b'success')
        except ConnectionRefusedError as e:
            msg = 'proxyed machine failed to connect to port '
            msg += str(natdata.port)
            msg += '\n' + str(e)
            s.sendall(msg.encode('utf-8'))
            print(e.args)
            return

        while True:
            # continuously receive request from proxy server.
            req = s.recv(TCP_MAX_SIZE)
            print('receive request from proxy server.')
            #print(req)
            #print('=========================')
            if not req:
                print('disconnected with proxy server')
                break

            # send request to native port.
            print('send request to native port.')
            try:
                s1.sendall(req)
            except:
                print('xxxxxxxxxx except xxxxxxxxxxx')
                s1.close()
                s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s1.connect((socket.gethostname(), natdata.port))
                s1.sendall(req)

            handle_response(proxy_socket=s, native_socket=s1)

        s1.close()
        s.close()


def change_port(natdata):
    port_str = input('new port: ')
    while not port_str.isdigit():
        print('input error, please check.')
        port_str = input('new port: ')

    natdata.port = int(port_str)
    print('Successfully!')


def clear_screen():
    system = platform.system()
    if system == 'Linux':
        os.system('clear')
    elif system == 'Windows':
        os.system('cls')
    else:
        print('unknown system')


def main():
    print('Welcome to natbreak (version 1.0.0)\n')

    print(platform.platform())
    print()

    print('Natbreak is actually the bridge of external network links.')
    print('After the client links the natbreak server,' +
          ' a tunnel is established. When visiting the tunnel website,' +
          ' the natbreak server will forward the data to the client through' +
          ' the tunnel to realize the internal network penetration.')

    natdata = NatData()

    while True:
        print('\n')
        command = input('Command (m for help): ')
        print()
        if not command:
            continue
        if command[0] == 'm':
            command_menu()
        elif command[0] == 'g':
            natdata.username = input('username: ')
            natdata.password = input('password: ')
            _thread.start_new_thread(start_proxy, (natdata, ))
        elif command[0] == 'p':
            change_port(natdata)
        elif command[0] == 'l':
            natdata.show_info()
        elif command[0] == 'c':
            clear_screen()
        elif command[0] == 'q':
            break
        else:
            print(command[0] + ': unknown command')
            print('Goodbye!')

if __name__ == "__main__":
    main()
