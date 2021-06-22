import unittest

from galileosky import tags, Packet


class TestTags(unittest.TestCase):
    def test_tags(self):
        for tag in tags.tags.values():
            value = tag.test_data()
            if value is None:
                continue

            data = tag.pack(value)
            self.assertDictEqual(value, tag.unpack(data)[0])

    def test_replace_tag_name(self):
        class Tag01(tags.Tag01):
            name = 'hw'

        self.assertTrue(tags.tags[Tag01.id].name == tags.Tag01.name)

        packet = Packet()
        packet.add(tags.Tag01.id, {tags.Tag01.name: 1})
        data, crc = packet.pack()
        headers, msgs = Packet.unpack(data)
        self.assertTrue(tags.Tag01.name in msgs[0][tags.Tag01.id])

        Packet.register(Tag01)

        headers, msgs = Packet.unpack(data)
        self.assertTrue(Tag01.name in msgs[0][tags.Tag01.id])
        self.assertTrue(tags.tags[Tag01.id].name == Tag01.name)
        Packet.register(tags.Tag01)

    def test_process_together(self):
        tag2_id = tags.Tag02.id
        old_name = tags.Tag02.name
        new_name = 'fw'
        add_name = 'fw_tag'
        tag1_value = 1
        tag2_value = 2

        class Tag02(tags.Tag02):
            @classmethod
            def to_dict(cls, value, msg, hp, conf):
                v = {new_name: value[0]}
                if (conf or {}).get('add_hw'):
                    v[add_name] = f'{msg[tags.Tag01.id][tags.Tag01.name]}:{v[new_name]}'
                else:
                    v[add_name] = '0'
                return v

        packet = Packet()
        packet.add(tags.Tag01.id, {tags.Tag01.name: tag1_value})
        packet.add(tag2_id, {old_name: tag2_value})
        data, crc = packet.pack()
        headers, msgs = Packet.unpack(data)
        self.assertTrue(old_name in msgs[0][tag2_id])
        self.assertTrue(add_name not in msgs[0][tag2_id])

        Packet.register(Tag02)

        headers, msgs = Packet.unpack(data)
        self.assertTrue(new_name in msgs[0][tag2_id])
        self.assertTrue(add_name in msgs[0][tag2_id])
        self.assertTrue(msgs[0][tag2_id][add_name] == '0')

        headers, msgs = Packet.unpack(data, {'add_hw': True})
        self.assertTrue(new_name in msgs[0][tag2_id])
        self.assertTrue(add_name in msgs[0][tag2_id])
        self.assertTrue(msgs[0][tag2_id][add_name] == f'{tag1_value}:{tag2_value}')

        Packet.register(tags.Tag02)
