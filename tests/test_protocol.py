from unittest import TestCase

from galileosky import Packet


class Test(TestCase):
    @staticmethod
    def x_str_to_bytes(data):
        return bytearray([int(data[i:i + 2], base=16) for i in range(0, len(data), 2)])

    def test_simple(self):
        msg = self.x_str_to_bytes('0117800182021003383632303537303437373435353331043200B548')

        headers, data = Packet.unpack(msg)
        packet = Packet()
        for k, v in data.items():
            packet.add(k, v)

        self.assertTrue(packet.pack() == msg)


