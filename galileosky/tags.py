import struct


class BaseTag(object):
    id = None
    format = None
    size = None

    @classmethod
    def pack(cls, data):
        return struct.pack('<B', cls.id) + struct.pack('<' + cls.format, data)

    @classmethod
    def unpack(cls, data, offset=0):
        return struct.unpack_from('<' + cls.format, data, offset=offset)[0]


class Tag01(BaseTag):
    id = 0x01
    format = 'B'


class Tag02(BaseTag):
    id = 0x02
    format = 'B'


class Tag03(BaseTag):
    id = 0x03
    format = '15s'


class Tag04(BaseTag):
    id = 0x04
    format = 'H'


class Tag10(BaseTag):
    id = 0x10
    format = 'H'


class Tag20(BaseTag):
    id = 0x20
    format = 'I'


class Tag30(BaseTag):
    id = 0x30
    format = 'BII'


class Tag33(BaseTag):
    id = 0x33
    format = 'HH'


class Tag34(BaseTag):
    id = 0x34
    format = 'H'


class Tag35(BaseTag):
    id = 0x35
    format = 'B'


class Tag40(BaseTag):
    id = 0x40
    format = 'H'


class Tag41(BaseTag):
    id = 0x41
    format = 'H'


class Tag42(BaseTag):
    id = 0x42
    format = 'H'


class Tag43(BaseTag):
    id = 0x43
    format = 'B'


class Tag44(BaseTag):
    id = 0x44
    format = 'I'


class Tag45(BaseTag):
    id = 0x45
    format = 'H'


class Tag46(BaseTag):
    id = 0x46
    format = 'H'


class Tag47(BaseTag):
    id = 0x47
    format = '4B'


class Tag50(BaseTag):
    id = 0x50
    format = 'H'


class Tag51(BaseTag):
    id = 0x51
    format = 'H'


class Tag52(BaseTag):
    id = 0x52
    format = 'H'


class Tag53(BaseTag):
    id = 0x53
    format = 'H'


class Tag54(BaseTag):
    id = 0x54
    format = 'H'


class Tag55(BaseTag):
    id = 0x55
    format = 'H'


class Tag56(BaseTag):
    id = 0x56
    format = 'H'


class Tag57(BaseTag):
    id = 0x57
    format = 'H'


class Tag58(BaseTag):
    id = 0x58
    format = 'H'


class Tag59(BaseTag):
    id = 0x59
    format = 'H'


class Tag5A(BaseTag):
    id = 0x5A
    format = 'I'


class Tag5B(BaseTag):
    id = 0x5B
    format = 'BH4B4H2B4H2B4H2B6H32B20B3I2H'


class Tag5C(BaseTag):
    id = 0x5C
    format = '34H'


class Tag5D(BaseTag):
    id = 0x5D
    format = 'HB'


class Tag60(BaseTag):
    id = 0x60
    format = 'H'


class Tag61(BaseTag):
    id = 0x61
    format = 'H'


class Tag62(BaseTag):
    id = 0x62
    format = 'H'


class Tag63(BaseTag):
    id = 0x63
    format = 'HB'


class Tag64(BaseTag):
    id = 0x64
    format = 'HB'


class Tag65(BaseTag):
    id = 0x65
    format = 'HB'


class Tag66(BaseTag):
    id = 0x66
    format = 'HB'


class Tag67(BaseTag):
    id = 0x67
    format = 'HB'


class Tag68(BaseTag):
    id = 0x68
    format = 'HB'


class Tag69(BaseTag):
    id = 0x69
    format = 'HB'


class Tag6A(BaseTag):
    id = 0x6A
    format = 'HB'


class Tag6B(BaseTag):
    id = 0x6B
    format = 'HB'


class Tag6C(BaseTag):
    id = 0x6C
    format = 'HB'


class Tag6D(BaseTag):
    id = 0x6D
    format = 'HB'


class Tag6E(BaseTag):
    id = 0x6E
    format = 'HB'


class Tag6F(BaseTag):
    id = 0x6F
    format = 'HB'


class Tag70(BaseTag):
    id = 0x70
    format = 'H'


class Tag71(BaseTag):
    id = 0x71
    format = 'H'


class Tag72(BaseTag):
    id = 0x72
    format = 'H'


class Tag73(BaseTag):
    id = 0x73
    format = 'H'


class Tag74(BaseTag):
    id = 0x74
    format = 'H'


class Tag75(BaseTag):
    id = 0x75
    format = 'H'


class Tag76(BaseTag):
    id = 0x76
    format = 'H'


class Tag77(BaseTag):
    id = 0x77
    format = 'H'


class Tag78(BaseTag):
    id = 0x78
    format = 'H'


class Tag79(BaseTag):
    id = 0x79
    format = 'H'


class Tag80(BaseTag):
    id = 0x80
    format = '3B'


class Tag81(BaseTag):
    id = 0x81
    format = '3B'


class Tag82(BaseTag):
    id = 0x82
    format = '3B'


class Tag83(BaseTag):
    id = 0x83
    format = '3B'


class Tag84(BaseTag):
    id = 0x84
    format = '3B'


class Tag85(BaseTag):
    id = 0x85
    format = '3B'


class Tag86(BaseTag):
    id = 0x86
    format = '3B'


class Tag87(BaseTag):
    id = 0x87
    format = '3B'


class Tag88(BaseTag):
    id = 0x88
    format = 'B'


class Tag89(BaseTag):
    id = 0x89
    format = 'B'


class Tag8A(BaseTag):
    id = 0x8A
    format = 'B'


class Tag8B(BaseTag):
    id = 0x8B
    format = 'B'


class Tag8C(BaseTag):
    id = 0x8C
    format = 'B'


class Tag90(BaseTag):
    id = 0x90
    format = 'I'


class TagA0(BaseTag):
    id = 0xA0
    format = 'B'


class TagA1(BaseTag):
    id = 0xA1
    format = 'B'


class TagA2(BaseTag):
    id = 0xA2
    format = 'B'


class TagA3(BaseTag):
    id = 0xA3
    format = 'B'


class TagA4(BaseTag):
    id = 0xA4
    format = 'B'


class TagA5(BaseTag):
    id = 0xA5
    format = 'B'


class TagA6(BaseTag):
    id = 0xA6
    format = 'B'


class TagA7(BaseTag):
    id = 0xA7
    format = 'B'


class TagA8(BaseTag):
    id = 0xA8
    format = 'B'


class TagA9(BaseTag):
    id = 0xA9
    format = 'B'


class TagAA(BaseTag):
    id = 0xAA
    format = 'B'


class TagAB(BaseTag):
    id = 0xAB
    format = 'B'


class TagAC(BaseTag):
    id = 0xAC
    format = 'B'


class TagAD(BaseTag):
    id = 0xAD
    format = 'B'


class TagAE(BaseTag):
    id = 0xAE
    format = 'B'


class TagAF(BaseTag):
    id = 0xAF
    format = 'B'


class TagB0(BaseTag):
    id = 0xB0
    format = 'H'


class TagB1(BaseTag):
    id = 0xB1
    format = 'H'


class TagB2(BaseTag):
    id = 0xB2
    format = 'H'


class TagB3(BaseTag):
    id = 0xB3
    format = 'H'


class TagB4(BaseTag):
    id = 0xB4
    format = 'H'


class TagB5(BaseTag):
    id = 0xB5
    format = 'H'


class TagB6(BaseTag):
    id = 0xB6
    format = 'H'


class TagB7(BaseTag):
    id = 0xB7
    format = 'H'


class TagB8(BaseTag):
    id = 0xB8
    format = 'H'


class TagB9(BaseTag):
    id = 0xB9
    format = 'H'


class TagC0(BaseTag):
    id = 0xC0
    format = 'I'


class TagC1(BaseTag):
    id = 0xC1
    format = 'I'


class TagC2(BaseTag):
    id = 0xC2
    format = 'I'


class TagC3(BaseTag):
    id = 0xC3
    format = 'I'


class TagC4(BaseTag):
    id = 0xC4
    format = 'B'


class TagC5(BaseTag):
    id = 0xC5
    format = 'B'


class TagC6(BaseTag):
    id = 0xC6
    format = 'B'


class TagC7(BaseTag):
    id = 0xC7
    format = 'B'


class TagC8(BaseTag):
    id = 0xC8
    format = 'B'


class TagC9(BaseTag):
    id = 0xC9
    format = 'B'


class TagCA(BaseTag):
    id = 0xCA
    format = 'B'


class TagCB(BaseTag):
    id = 0xCB
    format = 'B'


class TagCC(BaseTag):
    id = 0xCC
    format = 'B'


class TagCE(BaseTag):
    id = 0xCE
    format = 'B'


class TagCF(BaseTag):
    id = 0xCF
    format = 'B'


class TagD0(BaseTag):
    id = 0xD0
    format = 'B'


class TagD1(BaseTag):
    id = 0xD1
    format = 'B'


class TagD2(BaseTag):
    id = 0xD2
    format = 'B'


class TagD3(BaseTag):
    id = 0xD3
    format = 'I'


class TagD4(BaseTag):
    id = 0xD4
    format = 'I'


class TagD5(BaseTag):
    id = 0xD5
    format = 'B'


class TagD6(BaseTag):
    id = 0xD6
    format = 'H'


class TagD7(BaseTag):
    id = 0xD7
    format = 'H'


class TagD8(BaseTag):
    id = 0xD8
    format = 'H'


class TagD9(BaseTag):
    id = 0xD9
    format = 'H'


class TagDA(BaseTag):
    id = 0xDA
    format = 'H'


class TagDB(BaseTag):
    id = 0xDB
    format = 'I'


class TagDC(BaseTag):
    id = 0xDC
    format = 'I'


class TagDD(BaseTag):
    id = 0xDD
    format = 'I'


class TagDE(BaseTag):
    id = 0xDE
    format = 'I'


class TagDF(BaseTag):
    id = 0xDF
    format = 'I'


class TagE2(BaseTag):
    id = 0xE2
    format = 'I'


class TagE3(BaseTag):
    id = 0xE3
    format = 'I'


class TagE4(BaseTag):
    id = 0xE4
    format = 'I'


class TagE5(BaseTag):
    id = 0xE5
    format = 'I'


class TagE6(BaseTag):
    id = 0xE6
    format = 'I'


class TagE7(BaseTag):
    id = 0xE7
    format = 'I'


class TagE8(BaseTag):
    id = 0xE8
    format = 'I'


class TagE9(BaseTag):
    id = 0xE9
    format = 'I'


class TagEA(BaseTag):
    id = 0xEA
    format = '2B4BHH4BHH4BHH4BHH4BHH4BHH4BHH4BHH'


class TagF0(BaseTag):
    id = 0xF0
    format = 'I'


class TagF1(BaseTag):
    id = 0xF1
    format = 'I'


class TagF2(BaseTag):
    id = 0xF2
    format = 'I'


class TagF3(BaseTag):
    id = 0xF3
    format = 'I'


class TagF4(BaseTag):
    id = 0xF4
    format = 'I'


class TagF5(BaseTag):
    id = 0xF5
    format = 'I'


class TagF6(BaseTag):
    id = 0xF6
    format = 'I'


class TagF7(BaseTag):
    id = 0xF7
    format = 'I'


class TagF8(BaseTag):
    id = 0xF8
    format = 'I'


class TagF9(BaseTag):
    id = 0xF9
    format = 'I'


tags = {}
for c in BaseTag.__subclasses__():
    c.size = struct.calcsize('<' + c.format)
    tags[c.id] = c
