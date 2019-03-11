from ttbox_lib import GmeChecksumChunk
from unittest import TestCase


class TestGmeChecksumChunk(TestCase):
    def test_instantiation(self):
        GmeChecksumChunk(0x20, '\x12\x34\x56\x78')

    def test_instantiation_buffer_too_small(self):
        with self.assertRaises(RuntimeError) as context:
            GmeChecksumChunk(0x20, 'ABC')
        assert 'length 4' in str(context.exception)

    def test_instantiation_buffer_too_big(self):
        with self.assertRaises(RuntimeError) as context:
            GmeChecksumChunk(0x20, 'ABCDE')
        assert 'length 4' in str(context.exception)
