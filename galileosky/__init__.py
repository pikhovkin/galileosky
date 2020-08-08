import struct
from collections import OrderedDict

import libscrc

from .tags import tags as TAGS


__all__ = (
    'TagDoesNotExist',
    'Packet',
)


class TagDoesNotExist(Exception):
    pass


class Packet(object):
    def __init__(self):
        self._tags: list = []

    def add(self, tag: int, data):
        if tag not in TAGS:
            raise TagDoesNotExist(f'Tag {tag} does not exist')
        # TODO: Check data
        self._tags.append((tag, data))

    def pack(self, is_archive: bool=True, compress: bool=False, encrypt: bool=True):
        packet = struct.pack('<B', 1)
        tags = b''
        for t, data in self._tags:
            tags += TAGS[t].pack(data)

        mask = 0b1000000000000000 if is_archive else 0b0000000000000000
        len_packet = len(tags) | mask
        packet += struct.pack('<H', len_packet)
        packet += tags
        crc16 = libscrc.modbus(packet)
        packet += struct.pack('<H', crc16)
        return packet, crc16

    @staticmethod
    def unpack(data: bytes, compress: bool=False, encrypt: bool=True):
        h, len_pack = struct.unpack_from('<BH', data)
        length = len_pack & 0b0111111111111111
        is_archive = len_pack & 0b1000000000000000 == 0b1000000000000000
        crc16 = struct.unpack('<H', data[-2:])[0]
        headers = {
            'header': h,
            'length': length,
            'is_archive': is_archive,
            'crc16': crc16,
        }
        body = data[3:-2]
        offset = 0
        tags = OrderedDict()
        while offset < len(body):
            b = body[offset]
            tag = TAGS[b]
            value = tag.unpack(body, offset=offset + 1)
            offset += tag.size + 1
            tags[tag.id] = value

        return headers, tags

    @staticmethod
    def answer(crc16):
        return struct.pack('<B', 2) + struct.pack('<H', crc16)
