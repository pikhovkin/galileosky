import socket
import socketserver
from threading import Thread
from contextlib import contextmanager
import unittest
from queue import Queue
import random
import struct

from galileosky import Packet


HOST = 'localhost'
PORT = 38300


class SimpleTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        headers, tags = Packet.unpack(data)
        self.request.send(Packet.confirm(headers['crc16']))


class SimpleTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    request_queue_size = 1000
    daemon_threads = True


class TestSimpleServer(unittest.TestCase):
    @staticmethod
    @contextmanager
    def server(server_cls, handler_cls):
        server = server_cls((HOST, PORT), handler_cls)
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        yield server
        server.server_close()

    def test_load(self):
        class Terminal(Thread):
            def __init__(self, q_input, q_output):
                self.q_input = q_input
                self.q_output = q_output

                super(Terminal, self).__init__()

            def run(self):
                tasks = self.q_input.get()
                while tasks > 0:
                    tasks -= 1

                    packet = Packet()
                    packet.add(1, random.randrange(0, 256))
                    packet.add(2, random.randrange(0, 256))
                    packet.add(3, '862057047745531')
                    packet.add(0x04, random.randrange(0, 256))
                    true_data, crc16 = packet.pack()

                    if random.randrange(0, 2):
                        data = bytearray(true_data)
                        data[-1] = 0
                    else:
                        data = true_data

                    answer = 0
                    while answer != crc16:
                        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        tcp_client.connect((HOST, PORT))
                        tcp_client.sendall(data)
                        received = tcp_client.recv(4)
                        header, answer = struct.unpack_from('<BH', received)
                        if answer != crc16:
                            data = true_data
                        self.q_output.put(answer == crc16)
                        tcp_client.close()

                self.q_input.task_done()

        q_input = Queue()
        q_output = Queue()

        CLIENTS = 1000
        MESSAGES = 10

        for r in range(CLIENTS):
            q_input.put(MESSAGES)

        with self.server(SimpleTCPServer, SimpleTCPRequestHandler):
            for r in range(CLIENTS):
                w = Terminal(q_input, q_output)
                w.setDaemon(True)
                w.start()

            q_input.join()

        self.assertTrue(len(list(filter(bool, q_output.queue))) == CLIENTS * MESSAGES)
