import struct
from decimal import Decimal
from typing import Dict, Optional, Tuple
import random


class AutoFormat(object):
    @staticmethod
    def less_than_8_bytes(b):
        if b == 0:
            return ''
        elif b == 1:
            return 'B'
        elif b == 2:
            return 'H'
        elif b == 3:
            return 'HB'
        elif b == 4:
            return 'I'
        elif b == 5:
            return 'IB'
        elif b == 6:
            return 'IH'
        elif b == 7:
            return 'IHB'
        return ''

    @classmethod
    def for_pack(cls, data):
        f = ''
        for v in data:
            if isinstance(v, int):
                f += 'q' if v < 0 else 'Q'
            else:
                f += 'd'
        return f

    @classmethod
    def for_unpack(cls, length):
        size, m = divmod(length, 8)
        return f"{'Q' * size}{cls.less_than_8_bytes(m)}"


class BaseTag(object):
    id = 0
    format = ''
    size = 0
    name = ''

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return (int(value[cls.name]),)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {cls.name: value[0]}

    @classmethod
    def pack(cls, value, conf: Optional[Dict]=None) -> bytes:
        data = cls.from_dict(value, conf or {})
        return struct.pack(f'<{cls.format}', *data)

    @classmethod
    def unpack(
            cls,
            value: bytes,
            offset: int=0,
            record: Optional[Dict]=None,
            header_packet: Optional[Dict]=None,
            conf: Optional[Dict]=None
    ) -> Tuple[Dict, int]:
        data = struct.unpack_from(f'<{cls.format}', value, offset=offset)
        return cls.to_dict(data, record or {}, header_packet or {}, conf or {}), cls.size

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {cls.name: random.randrange(256)}


class Tag01(BaseTag):
    id = 0x01
    format = 'B'
    name = 'hardware'


class Tag02(BaseTag):
    id = 0x02
    format = 'B'
    name = 'firmware'


class Tag03(BaseTag):
    id = 0x03
    format = '15s'
    name = 'imei'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        imei = value[cls.name]
        if isinstance(imei, str):
            imei = imei.encode('utf-8')
        return (imei,)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {cls.name: value[0].decode('utf-8')}

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            cls.name: ''.join([str(random.randrange(0, 10)) for i in range(15)])
        }


class Tag04(BaseTag):
    id = 0x04
    format = 'H'
    name = 'terminal_id'


class Tag10(BaseTag):
    id = 0x10
    format = 'H'
    name = 'msg_id'


class Tag20(BaseTag):
    id = 0x20
    format = 'I'
    name = 'time'
    # time.strftime('%Y-%m%dT%H:%M:%S', time.gmtime(1))


class Tag30(BaseTag):
    id = 0x30
    format = 'Bii'
    name = 'navigation'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        B1 = ((value['source_type'] & 0xf) << 4) | (value['nsat'] & 0xf)
        lat = int(Decimal(str(value['lat'])) * 1000000)
        lon = int(Decimal(str(value['lon'])) * 1000000)
        return (B1, lat, lon)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            nsat=value[0] & 0xf,
            source_type=(value[0] & 0xf0) >> 4,
            lat=value[1] / 1000000,
            lon=value[2] / 1000000,
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'nsat': int(random.randrange(0, 16)),
            'source_type': int(random.randrange(0, 16)),
            'lat': int(random.random() * random.choice((-1, 1)) * 100000000) / 1000000,
            'lon': int(random.random() * random.choice((-1, 1)) * 100000000) / 1000000,
        }


class Tag33(BaseTag):
    id = 0x33
    format = 'HH'
    name = 'velocity'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return int(value['speed'] * 10), int(value['course'] * 10)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            speed=value[0] / 10,  # km/h
            course=value[1] / 10,  # degrees
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'speed': random.randrange(60),
            'course': random.randrange(360),
        }


class Tag34(BaseTag):
    id = 0x34
    format = 'h'
    name = 'height'  # meters

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag35(BaseTag):
    id = 0x35
    format = 'B'
    name = 'hdop'


class Tag40(BaseTag):
    id = 0x40
    format = 'H'
    name = 'status'  # terminal status


class Tag41(BaseTag):
    id = 0x41
    format = 'H'
    name = 'voltage'  # mV; terminal voltage


class Tag42(BaseTag):
    id = 0x42
    format = 'H'
    name = 'battery'  # mV; battery voltage


class Tag43(BaseTag):
    id = 0x43
    format = 'b'
    name = 't'  # °С

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag44(BaseTag):
    id = 0x44
    format = 'I'
    name = 'acceleration'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        a_x = value['a_x'] & 0x3ff
        a_y = (value['a_y'] & 0x3ff) << 10
        a_z = (value['a_z'] & 0x3ff) << 20
        return (a_z | a_y | a_x,)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            a_x=value[0] & 0x3ff,
            a_y=(value[0] & 0xffc00) >> 10,
            a_z=(value[0] & 0x3ff00000) >> 20,
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'a_x': random.randrange(256),
            'a_y': random.randrange(256),
            'a_z': random.randrange(256),
        }


class Tag45(BaseTag):
    id = 0x45
    format = 'H'
    name = 'outputs_status'


class Tag46(BaseTag):
    id = 0x46
    format = 'H'
    name = 'inputs_status'


class Tag47(BaseTag):
    id = 0x47
    format = '4B'
    name = 'ecodrive'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        ed_a = int(Decimal(str(value['ecodrive_acceleration'])) * 100)
        ed_dea = int(Decimal(str(value['ecodrive_deceleration'])) * 100)
        ed_aa = int(Decimal(str(value['ecodrive_angle_acceleration'])) * 100)
        ed_bump = int(Decimal(str(value['ecodrive_bump'])) * 100)
        return (ed_a, ed_dea, ed_aa, ed_bump)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            ecodrive_acceleration=value[0] / 100,  # g = m/s^2
            ecodrive_deceleration=value[1] / 100,  # g = m/s^2
            ecodrive_angle_acceleration=value[2] / 100,  # g = m/s^2
            ecodrive_bump=value[3] / 100,  # g = m/s^2
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'ecodrive_acceleration': random.randrange(100, 256, 5) / 100,
            'ecodrive_deceleration': random.randrange(100, 256, 5) / 100,
            'ecodrive_angle_acceleration': random.randrange(100, 256, 5) / 100,
            'ecodrive_bump': random.randrange(100, 256, 5) / 100,
        }


class Tag48(BaseTag):
    id = 0x48
    format = 'H'
    name = 'ext_status'  # extended status of terminal


class Tag50(BaseTag):
    id = 0x50
    format = 'H'
    name = 'input0'


class Tag51(BaseTag):
    id = 0x51
    format = 'H'
    name = 'input1'


class Tag52(BaseTag):
    id = 0x52
    format = 'H'
    name = 'input2'


class Tag53(BaseTag):
    id = 0x53
    format = 'H'
    name = 'input3'


class Tag54(BaseTag):
    id = 0x54
    format = 'H'
    name = 'input4'


class Tag55(BaseTag):
    id = 0x55
    format = 'H'
    name = 'input5'


class Tag56(BaseTag):
    id = 0x56
    format = 'H'
    name = 'input6'


class Tag57(BaseTag):
    id = 0x57
    format = 'H'
    name = 'input7'


class Tag58(BaseTag):
    id = 0x58
    format = 'H'
    name = 'rs232_0'


class Tag59(BaseTag):
    id = 0x59
    format = 'H'
    name = 'rs232_1'


class Tag5A(BaseTag):
    id = 0x5A
    format = 'I'
    name = 'electric_meter'


class Tag5B(BaseTag):
    id = 0x5B
    format = 'BH4B4H2B4H2B4H2B6H32B20B3I2H'
    name = 'refrigerator'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {}  # TODO: !!!

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return


class Tag5C(BaseTag):
    id = 0x5C
    format = '34H'
    name = 'ppro'  # PressurePro

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        if not value:
            return (255,)

        data = []
        for i in range(34):
            press = value[f'{cls.name}{i}_press']
            t = int((value[f'{cls.name}{i}_t'] + 40) / 20) & 0xff
            link = (value[f'{cls.name}{i}_link'] & 0xff) << 3
            fail = (value[f'{cls.name}{i}_fail'] & 0xff) << 4
            cause = (value[f'{cls.name}{i}_cause'] & 0xff) << 5
            state = cause | fail | link | t
            data.append((state << 8) | (press & 0xff))
        return tuple(data)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        if len(value) == 1:
            return {}

        data = {}
        for i, v in enumerate(value):
            state = (v & 0xff00) >> 8
            data.update({
                f'{cls.name}{i}_press': v & 0xff,  # psi, lbs
                f'{cls.name}{i}_t': (state & 0x07) * 20 - 40,  # °С
                f'{cls.name}{i}_link': (state & 0x08) >> 3,
                f'{cls.name}{i}_fail': (state & 0x10) >> 4,
                f'{cls.name}{i}_cause': (state & 0xe0) >> 5,
            })
        return data

    @classmethod
    def pack(cls, value, conf: Optional[Dict] = None) -> bytes:
        data = cls.from_dict(value, conf or {})
        format = 'H' if len(data) == 1 else cls.format
        return struct.pack(f'<{format}', *data)

    @classmethod
    def unpack(
            cls,
            value: bytes,
            offset: int=0,
            record: Optional[Dict]=None,
            header_packet: Optional[Dict]=None,
            conf: Optional[Dict]=None
    ) -> Tuple[Dict, int]:
        format = 'H' if value[offset:offset + 2] == b'\xff\x00' else cls.format
        data = struct.unpack_from(f'<{format}', value, offset=offset)
        return cls.to_dict(data, record or {}, header_packet or {}, conf or {}), cls.size

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        if not random.randrange(2):
            return {}

        data = {}
        for i in range(34):
            data.update({
                f'{cls.name}{i}_press': random.randrange(256),
                f'{cls.name}{i}_t': random.randrange(-40, 101, 20),
                f'{cls.name}{i}_link': random.randrange(2),
                f'{cls.name}{i}_fail': random.randrange(2),
                f'{cls.name}{i}_cause': random.randrange(7),
            })
        return data


class Tag5D(BaseTag):
    id = 0x5D
    format = 'HB'
    name = 'dosimeter'  # Sv/h

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {}  # TODO:

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return


class Tag60(BaseTag):
    id = 0x60
    format = 'H'
    name = 'rs485_0_fuel'


class Tag61(BaseTag):
    id = 0x61
    format = 'H'
    name = 'rs485_1_fuel'


class Tag62(BaseTag):
    id = 0x62
    format = 'H'
    name = 'rs485_2_fuel'


class Tag63(BaseTag):
    id = 0x63
    format = 'Hb'
    name = 'rs485_3'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return (int(value[f'{cls.name}_fuel']), int(value[f'{cls.name}_t']))

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {
            f'{cls.name}_fuel': value[0],  # liters
            f'{cls.name}_t': value[1],  # °С
        }

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            f'{cls.name}_fuel': random.randrange(256),
            f'{cls.name}_t': random.randrange(-128, 128),
        }


class Tag64(Tag63):
    id = 0x64
    format = 'Hb'
    name = 'rs485_4'


class Tag65(Tag63):
    id = 0x65
    format = 'Hb'
    name = 'rs485_5'


class Tag66(Tag63):
    id = 0x66
    format = 'Hb'
    name = 'rs485_6'


class Tag67(Tag63):
    id = 0x67
    format = 'Hb'
    name = 'rs485_7'


class Tag68(Tag63):
    id = 0x68
    format = 'Hb'
    name = 'rs485_8'


class Tag69(Tag63):
    id = 0x69
    format = 'Hb'
    name = 'rs485_9'


class Tag6A(Tag63):
    id = 0x6A
    format = 'Hb'
    name = 'rs485_10'


class Tag6B(Tag63):
    id = 0x6B
    format = 'Hb'
    name = 'rs485_11'


class Tag6C(Tag63):
    id = 0x6C
    format = 'Hb'
    name = 'rs485_12'


class Tag6D(Tag63):
    id = 0x6D
    format = 'Hb'
    name = 'rs485_13'


class Tag6E(Tag63):
    id = 0x6E
    format = 'Hb'
    name = 'rs485_14'


class Tag6F(Tag63):
    id = 0x6F
    format = 'Hb'
    name = 'rs485_15'


class Tag70(BaseTag):
    id = 0x70
    format = 'Bb'
    name = 'thermometer0'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return (int(value[f'{cls.name}_id']), int(value[f'{cls.name}_t']))

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {
            f'{cls.name}_id': value[0],
            f'{cls.name}_t': value[1],
        }

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            f'{cls.name}_id': random.randrange(256),
            f'{cls.name}_t': random.randrange(-128, 128),
        }


class Tag71(Tag70):
    id = 0x71
    format = 'Bb'
    name = 'thermometer1'


class Tag72(Tag70):
    id = 0x72
    format = 'Bb'
    name = 'thermometer2'


class Tag73(Tag70):
    id = 0x73
    format = 'Bb'
    name = 'thermometer3'


class Tag74(Tag70):
    id = 0x74
    format = 'Bb'
    name = 'thermometer4'


class Tag75(Tag70):
    id = 0x75
    format = 'Bb'
    name = 'thermometer5'


class Tag76(Tag70):
    id = 0x76
    format = 'Bb'
    name = 'thermometer6'


class Tag77(Tag70):
    id = 0x77
    format = 'Bb'
    name = 'thermometer7'


class Tag78(BaseTag):
    id = 0x78
    format = 'H'
    name = 'input8'


class Tag79(BaseTag):
    id = 0x79
    format = 'H'
    name = 'input9'


class Tag80(BaseTag):
    id = 0x80
    format = 'BbB'
    name = 'ds1923_0'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return (int(value[f'{cls.name}_id']),
                int(value[f'{cls.name}_t']),
                int(value[f'{cls.name}_humidity'] * 255 / 100))

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {
            f'{cls.name}_id': value[0],
            f'{cls.name}_t': value[1],  # °С
            f'{cls.name}_humidity': value[2] * 100 / 255,  # %
        }

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            f'{cls.name}_id': random.randrange(256),
            f'{cls.name}_t': random.randrange(-128, 128),
            f'{cls.name}_humidity': random.randrange(0, 101, 20),
        }


class Tag81(Tag80):
    id = 0x81
    format = 'BbB'
    name = 'ds1923_1'


class Tag82(Tag80):
    id = 0x82
    format = 'BbB'
    name = 'ds1923_2'


class Tag83(Tag80):
    id = 0x83
    format = 'BbB'
    name = 'ds1923_3'


class Tag84(Tag80):
    id = 0x84
    format = 'BbB'
    name = 'ds1923_4'


class Tag85(Tag80):
    id = 0x85
    format = 'BbB'
    name = 'ds1923_5'


class Tag86(Tag80):
    id = 0x86
    format = 'BbB'
    name = 'ds1923_6'


class Tag87(Tag80):
    id = 0x87
    format = 'BbB'
    name = 'ds1923_7'


class Tag88(BaseTag):
    id = 0x88
    format = 'b'
    name = 'rs232_01_tw'

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag89(BaseTag):
    id = 0x89
    format = 'b'
    name = 'rs232_1_tw'

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag8A(BaseTag):
    id = 0x8A
    format = 'b'
    name = 'rs485_0_t'

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag8B(BaseTag):
    id = 0x8B
    format = 'b'
    name = 'rs485_1_t'

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag8C(BaseTag):
    id = 0x8C
    format = 'b'
    name = 'rs485_2_t'

    @classmethod
    def test_data(cls, conf: Optional[Dict] = None) -> Dict:
        return {cls.name: random.randrange(-128, 128)}


class Tag90(BaseTag):
    id = 0x90
    format = 'I'
    name = 'ibutton1'


class TagA0(BaseTag):
    id = 0xA0
    format = 'B'
    name = 'can8bitr15'


class TagA1(BaseTag):
    id = 0xA1
    format = 'B'
    name = 'can8bitr16'


class TagA2(BaseTag):
    id = 0xA2
    format = 'B'
    name = 'can8bitr17'


class TagA3(BaseTag):
    id = 0xA3
    format = 'B'
    name = 'can8bitr18'


class TagA4(BaseTag):
    id = 0xA4
    format = 'B'
    name = 'can8bitr19'


class TagA5(BaseTag):
    id = 0xA5
    format = 'B'
    name = 'can8bitr20'


class TagA6(BaseTag):
    id = 0xA6
    format = 'B'
    name = 'can8bitr21'


class TagA7(BaseTag):
    id = 0xA7
    format = 'B'
    name = 'can8bitr22'


class TagA8(BaseTag):
    id = 0xA8
    format = 'B'
    name = 'can8bitr23'


class TagA9(BaseTag):
    id = 0xA9
    format = 'B'
    name = 'can8bitr24'


class TagAA(BaseTag):
    id = 0xAA
    format = 'B'
    name = 'can8bitr25'


class TagAB(BaseTag):
    id = 0xAB
    format = 'B'
    name = 'can8bitr26'


class TagAC(BaseTag):
    id = 0xAC
    format = 'B'
    name = 'can8bitr27'


class TagAD(BaseTag):
    id = 0xAD
    format = 'B'
    name = 'can8bitr28'


class TagAE(BaseTag):
    id = 0xAE
    format = 'B'
    name = 'can8bitr29'


class TagAF(BaseTag):
    id = 0xAF
    format = 'B'
    name = 'can8bitr30'


class TagB0(BaseTag):
    id = 0xB0
    format = 'H'
    name = 'can16bitr5'


class TagB1(BaseTag):
    id = 0xB1
    format = 'H'
    name = 'can16bitr6'


class TagB2(BaseTag):
    id = 0xB2
    format = 'H'
    name = 'can16bitr7'


class TagB3(BaseTag):
    id = 0xB3
    format = 'H'
    name = 'can16bitr8'


class TagB4(BaseTag):
    id = 0xB4
    format = 'H'
    name = 'can16bitr9'


class TagB5(BaseTag):
    id = 0xB5
    format = 'H'
    name = 'can16bitr10'


class TagB6(BaseTag):
    id = 0xB6
    format = 'H'
    name = 'can16bitr11'


class TagB7(BaseTag):
    id = 0xB7
    format = 'H'
    name = 'can16bitr12'


class TagB8(BaseTag):
    id = 0xB8
    format = 'H'
    name = 'can16bitr13'


class TagB9(BaseTag):
    id = 0xB9
    format = 'H'
    name = 'can16bitr14'


class TagC0(BaseTag):
    id = 0xC0
    format = 'I'
    name = 'can_a0'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return (int(value['can_spent_fuel'] * 2),)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            can_spent_fuel=value[0] * 0.5,  # liters
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'can_spent_fuel': random.randrange(256),
        }


class TagC1(BaseTag):
    id = 0xC1
    format = 'BBH'
    name = 'can_a1'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        fuel_balance = value['can_fuel_balance'] / 0.4
        t = value['can_coolant_t'] + 40
        engine_speed = value['can_engine_speed'] / 0.125
        return (int(fuel_balance), int(t), int(engine_speed))

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            can_fuel_balance=value[0] * 0.4,  # %
            can_coolant_t=value[1] - 40,  # °C
            can_engine_speed=value[2] * 0.125,  # rpm
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'can_fuel_balance': random.randrange(0, 103, 2),
            'can_coolant_t': random.randrange(0, 256 - 40),
            'can_engine_speed': random.randrange(0, 256),
        }


class TagC2(BaseTag):
    id = 0xC2
    format = 'I'
    name = 'can_b0'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return (int(value['can_mileage'] / 5),)

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return dict(
            can_mileage=value[0] * 5,  # meters
        )

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {
            'can_mileage': random.randrange(0, 256, 5),
        }


class TagC3(BaseTag):
    id = 0xC3
    format = 'I'
    name = 'can_b1'


class TagC4(BaseTag):
    id = 0xC4
    format = 'B'
    name = 'can8bitr0'


class TagC5(BaseTag):
    id = 0xC5
    format = 'B'
    name = 'can8bitr1'


class TagC6(BaseTag):
    id = 0xC6
    format = 'B'
    name = 'can8bitr2'


class TagC7(BaseTag):
    id = 0xC7
    format = 'B'
    name = 'can8bitr3'


class TagC8(BaseTag):
    id = 0xC8
    format = 'B'
    name = 'can8bitr4'


class TagC9(BaseTag):
    id = 0xC9
    format = 'B'
    name = 'can8bitr5'


class TagCA(BaseTag):
    id = 0xCA
    format = 'B'
    name = 'can8bitr6'


class TagCB(BaseTag):
    id = 0xCB
    format = 'B'
    name = 'can8bitr7'


class TagCC(BaseTag):
    id = 0xCC
    format = 'B'
    name = 'can8bitr8'


class TagCD(BaseTag):
    id = 0xCD
    format = 'B'
    name = 'can8bitr9'


class TagCE(BaseTag):
    id = 0xCE
    format = 'B'
    name = 'can8bitr10'


class TagCF(BaseTag):
    id = 0xCF
    format = 'B'
    name = 'can8bitr11'


class TagD0(BaseTag):
    id = 0xD0
    format = 'B'
    name = 'can8bitr12'


class TagD1(BaseTag):
    id = 0xD1
    format = 'B'
    name = 'can8bitr13'


class TagD2(BaseTag):
    id = 0xD2
    format = 'B'
    name = 'can8bitr14'


class TagD3(BaseTag):
    id = 0xD3
    format = 'I'
    name = 'ibutton2'


class TagD4(BaseTag):
    id = 0xD4
    format = 'I'
    name = 'mileage'  # meters


class TagD5(BaseTag):
    id = 0xD5
    format = 'B'
    name = 'ibuttons'


class TagD6(BaseTag):
    id = 0xD6
    format = 'H'
    name = 'can16bitr0'


class TagD7(BaseTag):
    id = 0xD7
    format = 'H'
    name = 'can16bitr1'


class TagD8(BaseTag):
    id = 0xD8
    format = 'H'
    name = 'can16bitr2'


class TagD9(BaseTag):
    id = 0xD9
    format = 'H'
    name = 'can16bitr3'


class TagDA(BaseTag):
    id = 0xDA
    format = 'H'
    name = 'can16bitr4'


class TagDB(BaseTag):
    id = 0xDB
    format = 'I'
    name = 'can32bitr0'  # TODO: / 100; depends on settings


class TagDC(BaseTag):
    id = 0xDC
    format = 'I'
    name = 'can32bitr1'  # TODO: / 10; depends on settings


class TagDD(BaseTag):
    id = 0xDD
    format = 'I'
    name = 'can32bitr2'


class TagDE(BaseTag):
    id = 0xDE
    format = 'I'
    name = 'can32bitr3'


class TagDF(BaseTag):
    id = 0xDF
    format = 'I'
    name = 'can32bitr4'


class TagE2(BaseTag):
    id = 0xE2
    format = 'I'
    name = 'user_data0'


class TagE3(BaseTag):
    id = 0xE3
    format = 'I'
    name = 'user_data1'


class TagE4(BaseTag):
    id = 0xE4
    format = 'I'
    name = 'user_data2'


class TagE5(BaseTag):
    id = 0xE5
    format = 'I'
    name = 'user_data3'


class TagE6(BaseTag):
    id = 0xE6
    format = 'I'
    name = 'user_data4'


class TagE7(BaseTag):
    id = 0xE7
    format = 'I'
    name = 'user_data5'


class TagE8(BaseTag):
    id = 0xE8
    format = 'I'
    name = 'user_data6'


class TagE9(BaseTag):
    id = 0xE9
    format = 'I'
    name = 'user_data7'


class TagEA(BaseTag):
    id = 0xEA
    format = 'B'
    name = 'user_data_array'

    @classmethod
    def from_dict(cls, value: Dict, conf: Dict) -> Tuple:
        return tuple(value[cls.name])

    @classmethod
    def to_dict(cls, value: Tuple, record: Dict, header_packet: Dict, conf: Dict) -> Dict:
        return {cls.name: list(value)}

    @classmethod
    def pack(cls, value, conf: Optional[Dict] = None) -> bytes:
        data = cls.from_dict(value, conf or {})
        if cls is TagEA:
            sub_format = AutoFormat.for_pack(data)
        else:
            sub_format, data = data

        return struct.pack(f'<{cls.format}', struct.calcsize(f'<{sub_format}')) + struct.pack(f'<{sub_format}', *data)

    @classmethod
    def unpack(
            cls,
            value: bytes,
            offset: int = 0,
            record: Optional[dict] = None,
            header_packet: Optional[dict] = None,
            conf: Optional[dict] = None
    ) -> Tuple[dict, int]:
        data = struct.unpack_from(f'<{cls.format}', value, offset=offset)
        length = data[0]

        if cls is TagEA:
            sub_format = AutoFormat.for_unpack(length)
            data = struct.unpack_from(f'<{sub_format}', value, offset=offset + 1)
        else:
            body = value[offset + 1: offset + length + 1]
            data = (length, body)

        return cls.to_dict(data, record or {}, header_packet or {}, conf or {}), length + 1

    @classmethod
    def test_data(cls, conf: Optional[Dict]=None) -> Dict:
        return {cls.name: [8, 10, 0, 1000_000_000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


class TagF0(BaseTag):
    id = 0xF0
    format = 'I'
    name = 'can32bitr5'


class TagF1(BaseTag):
    id = 0xF1
    format = 'I'
    name = 'can32bitr6'


class TagF2(BaseTag):
    id = 0xF2
    format = 'I'
    name = 'can32bitr7'


class TagF3(BaseTag):
    id = 0xF3
    format = 'I'
    name = 'can32bitr8'


class TagF4(BaseTag):
    id = 0xF4
    format = 'I'
    name = 'can32bitr9'


class TagF5(BaseTag):
    id = 0xF5
    format = 'I'
    name = 'can32bitr10'


class TagF6(BaseTag):
    id = 0xF6
    format = 'I'
    name = 'can32bitr11'


class TagF7(BaseTag):
    id = 0xF7
    format = 'I'
    name = 'can32bitr12'


class TagF8(BaseTag):
    id = 0xF8
    format = 'I'
    name = 'can32bitr13'


class TagF9(BaseTag):
    id = 0xF9
    format = 'I'
    name = 'can32bitr14'


tags = {}
_tags = BaseTag.__subclasses__()
while _tags:
    t = _tags.pop(0)
    t.size = struct.calcsize(f'<{t.format}')
    tags[t.id] = t
    _tags.extend(t.__subclasses__())


__all__ = tuple(tags.values())
