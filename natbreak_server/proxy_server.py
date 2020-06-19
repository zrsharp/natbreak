#!/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
import random
import _thread
import user_service

TCP_MAX_SIZE = 1024 * 1024 * 2


class ProxyThread(threading.Thread):
    def __init__(self, proxy_socket, addr, proxy_dict):
        threading.Thread.__init__(self)
        # socket between proxy server and proxyed machine
        self._proxy_socket = proxy_socket
        self._addr = addr
        self._proxy_dict = proxy_dict
        # socket between proxy server and client machine
        self._subserver_socket = None
        self._used_traffic = 0

    def __deal_client_socket(self, client_socket, client_addr):
        print('Accepted a client:', str(client_addr))
        while True:
            # continuously receive data from client.
            req = client_socket.recv(TCP_MAX_SIZE)
            print('receive request from a client.')
            print(req)

            if not req:
                print('client closed the connect')
                break

            # send request to proxyed machine.
            print('sending request to proxyed machine.')
            self._proxy_socket.sendall(req)
            while True:
                # receive response from proxyed machine.
                rep = self._proxy_socket.recv(TCP_MAX_SIZE)
                print('received response from proxyed machine.')
                if not rep:
                    break

                # send response to client machine.
                client_socket.sendall(rep)
                # calculate traffic
                self._used_traffic += len(rep)

                if rep == b'zero\r\n\r\n':
                    break

            print('**********response successfully!**********')

        print('\nClient has been disconnected.')
        client_socket.close()


    def run(self):
        host = self._addr[0]
        port = self._addr[1]
        print('Accepted proxy:')
        print('host: ', host, '\nport', port)

        rep = self._proxy_socket.recv(TCP_MAX_SIZE)
        rep_str = rep.decode('utf-8')
        login_info = rep_str.split(' ')
        print(login_info)
        if len(login_info) != 2:
            self._proxy_socket.sendall('login error'.encode('utf-8'))
            return

        username = login_info[0]
        password = login_info[1]
        user = user_service.User(username, password)
        login_success = user.login()

        if not login_success:
            print('login fail')
            self._proxy_socket.sendall(
                'Login fail, check your password'.encode('utf-8'))
            self._proxy_socket.close()
            return

        # asign a random port.
        if len(self._proxy_dict) == 5000:
            print('Server congestion')
            self._proxy_socket.sendall('Server congestion.'.encode('utf-8'))
            return

        # create no repeat random number.
        subserver_port = random.randint(10000, 15000)
        while subserver_port in self._proxy_dict:
            subserver_port = random.randint(10000, 15000)

        # send hostname and assigned port
        # as login result to proxyed machine.
        self._proxy_socket.sendall(
            ('success\n%s\n%d' %
             (socket.gethostname(), subserver_port)).encode('utf-8'))

        # wait to receive ack from proxyed machine.
        proxyed_machine_ack = self._proxy_socket.recv(TCP_MAX_SIZE)
        if proxyed_machine_ack != b'success':
            print(proxyed_machine_ack)
            return

        print('proxyed machine ' + str(self._addr) + ' ack success')

        # socket to accept client request.
        self._subserver_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_STREAM)
        self._subserver_socket.bind((socket.gethostname(), subserver_port))
        self._subserver_socket.listen(1024)

        self._proxy_dict[subserver_port] = self

        print('success %d' % subserver_port)

        while True:
            try:
                # begin accept client request.
                client_socket, client_addr = self._subserver_socket.accept()
                # start a bew thread to deal with a client.
                _thread.start_new_thread(self.__deal_client_socket,
                                         (client_socket, client_addr))
            except BaseException as e:
                print(e)
                print('subserver_socket occured error!')
                break

            # test socket
            #self._proxy_socket.sendall('ping'.encode('utf-8'))
            #ping_result = self._proxy_socket.recv(TCP_MAX_SIZE)
            #if not ping_result:
            #    break

        self._subserver_socket.close()
        print('proxy', str(self._addr), 'stop')
        del self._proxy_dict[subserver_port]


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = socket.gethostname()
    PORT = 9000
    print('Proxy server started at:')
    print('host: ', HOST, '\nport: ', PORT)
    serversocket.bind((HOST, PORT))

    serversocket.listen(500)
    PROXY_DICT = {}

    print('======================================')

    while True:
        proxy_socket, addr = serversocket.accept()
        proxy_thread = ProxyThread(proxy_socket, addr, PROXY_DICT)
        proxy_thread.start()
        proxy_thread.join()


if __name__ == '__main__':
    main()
