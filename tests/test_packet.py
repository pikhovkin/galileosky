from unittest import TestCase

from galileosky import Packet


class Test(TestCase):
    def test_simple(self):
        msg = bytes.fromhex('0117800182021003383632303537303437373435353331043200B548')

        headers, data = Packet.unpack(msg)
        packet = Packet()
        for k, v in data.items():
            packet.add(k, v)

        data, crc16 = packet.pack()
        self.assertTrue(data == msg)
        self.assertTrue(headers['crc16'] == crc16)
