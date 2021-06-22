import struct
from collections import OrderedDict
from typing import Optional, Dict, Tuple

import libscrc

from .tags import tags as TAGS


__all__ = (
    'TagDoesNotExist',
    'CRCDoesNotMatch',
    'ExtractPacketFailed',
    'Packet',
)


class TagDoesNotExist(Exception):
    pass


class CRCDoesNotMatch(Exception):
    pass


class ExtractPacketFailed(Exception):
    pass


class Packet(object):
    TagDoesNotExist = TagDoesNotExist
    CRCDoesNotMatch = CRCDoesNotMatch
    ExtractPacketFailed = ExtractPacketFailed

    def __init__(self):
        self._tags: list = []

    def add(self, tag_id: int, data):
        if tag_id not in TAGS:
            raise TagDoesNotExist(f'Tag {tag_id} does not exist')
        # TODO: Check data
        self._tags.append((tag_id, data))

    def pack(self, is_archive: bool=True):
        packet = struct.pack('<B', 1)
        tags = b''
        for tag_id, data in self._tags:
            tags += struct.pack('<B', tag_id) + TAGS[tag_id].pack(data)

        mask = 0b1000000000000000 if is_archive else 0b0000000000000000
        len_packet = len(tags) | mask
        packet += struct.pack('<H', len_packet)
        packet += tags
        crc16 = libscrc.modbus(packet)
        packet += struct.pack('<H', crc16)
        return packet, crc16

    @staticmethod
    def unpack(data: bytes, conf: Optional[Dict]=None, header_packet: Optional[Dict]=None) -> Tuple:
        h, len_pack = struct.unpack_from('<BH', data)
        length = len_pack & 0b0111111111111111
        is_archive = len_pack & 0b1000000000000000 == 0b1000000000000000
        crc16 = struct.unpack_from('<H', data, offset=length + 3)[0]
        headers = {
            'header': h,
            'length': length,
            'is_archive': is_archive,
            'crc16': crc16,
        }
        body = data[3:length + 3]
        offset = 0
        hp = header_packet or OrderedDict()
        packet = []
        record = OrderedDict()
        last_tag_id = 0
        while offset < len(body):
            tag_id = body[offset]

            if last_tag_id >= tag_id:
                packet.append(record)
                record = OrderedDict()

            tag = TAGS[tag_id]
            value, size = tag.unpack(body, offset=offset + 1, record=record, header_packet=hp, conf=conf or {})
            offset += size + 1
            record[tag.id] = value
            last_tag_id = tag_id

        if record:
            packet.append(record)

        return headers, packet

    @staticmethod
    def confirm(crc16: int) -> bytes:
        return struct.pack('<B', 2) + struct.pack('<H', crc16)

    @staticmethod
    def check_crc(crc16: int, data: bytes):
        header, answer = struct.unpack_from('<BH', data)
        if answer != crc16:
            raise CRCDoesNotMatch('CRC16 does not match')

    @classmethod
    def extract(cls, data: bytes, header_packet: Optional[Dict]=None) -> Tuple:
        try:
            return cls.unpack(data, header_packet=header_packet)
        except struct.error:
            raise ExtractPacketFailed('Extract packet failed')

    @staticmethod
    def register(tag):
        tag.size = struct.calcsize(f'<{tag.format}')
        TAGS[tag.id] = tag
