import unittest

from galileosky import tags


class TestTags(unittest.TestCase):
    def test_tags(self):
        for tag in tags.tags.values():
            value = tag.test_data()
            if value is None:
                continue

            data = tag.pack(value)
            self.assertDictEqual(value, tag.unpack(data))
