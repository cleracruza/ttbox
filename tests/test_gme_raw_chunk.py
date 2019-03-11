from ttbox_lib import GmeRawChunk
from StringIO import StringIO
from unittest import TestCase


class TestGmeRawChunk(TestCase):
    def test_kind_to_cls_raw(self):
        chunk = GmeRawChunk(0x20, '\x12')
        cls = chunk.kind_to_cls('raw')
        assert cls.__name__ == 'GmeRawChunk'

    def test_kind_to_cls_checksum(self):
        chunk = GmeRawChunk(0x20, '\x12')
        cls = chunk.kind_to_cls('checksum')
        assert cls.__name__ == 'GmeChecksumChunk'

    def test_set_int32_normal(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        chunk.set_int32(1, 0x12345678)
        assert chunk.buffer == 'A\x78\x56\x34\x12F'

    def test_set_int32_small(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        chunk.set_int32(1, 0x78)
        assert chunk.buffer == 'A\x78\x00\x00\x00F'

    def test_set_int32_at_end(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        chunk.set_int32(2, 0x12345678)
        assert chunk.buffer == 'AB\x78\x56\x34\x12'

    def test_set_int32_past_end(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        with self.assertRaises(RuntimeError) as context:
            chunk.set_int32(3, 0x12345678)
        assert 'past chunk end' in str(context.exception)

    def test_set_int32_at_start(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        chunk.set_int32(0, 0x12345678)
        assert chunk.buffer == '\x78\x56\x34\x12EF'

    def test_set_int32_before_start(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        with self.assertRaises(RuntimeError) as context:
            chunk.set_int32(-7, 0x12345678)
        assert 'before chunk start' in str(context.exception)

    def test_set_int32_in_too_small_buffer(self):
        chunk = GmeRawChunk(0x20, 'ABC')
        with self.assertRaises(RuntimeError) as context:
            chunk.set_int32(-2, 0x12345678)
        assert 'chunk size' in str(context.exception)

    def test_get_int32_normal(self):
        chunk = GmeRawChunk(0x20, 'A\x78\x56\x34\x12F')
        assert chunk.get_int32(1) == 0x12345678

    def test_get_int32_small(self):
        chunk = GmeRawChunk(0x20, 'A\x78\x00\x34\x00F')
        assert chunk.get_int32(1) == 0x340078

    def test_get_int32_at_end(self):
        chunk = GmeRawChunk(0x20, 'A\x78\x56\x34\x12')
        assert chunk.get_int32(1) == 0x12345678

    def test_get_int32_past_end(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        with self.assertRaises(RuntimeError) as context:
            chunk.get_int32(3)
        assert 'past chunk end' in str(context.exception)

    def test_get_int32_at_start(self):
        chunk = GmeRawChunk(0x20, '\x78\x56\x34\x12F')
        assert chunk.get_int32(0) == 0x12345678

    def test_get_int32_before_start(self):
        chunk = GmeRawChunk(0x20, 'ABCDEF')
        with self.assertRaises(RuntimeError) as context:
            chunk.get_int32(-7)
        assert 'before chunk start' in str(context.exception)

    def test_get_int32_in_too_small_buffer(self):
        chunk = GmeRawChunk(0x20, 'ABC')
        with self.assertRaises(RuntimeError) as context:
            chunk.get_int32(-2)
        assert 'chunk size' in str(context.exception)

    def test_checksum_single(self):
        chunk = GmeRawChunk(0x20, '\x12')
        assert chunk.checksum() == 18

    def test_checksum_multiple(self):
        chunk = GmeRawChunk(0x20, '\x7F\x12\x80')
        assert chunk.checksum() == 273

    def test_write(self):
        buffer = StringIO()

        chunk = GmeRawChunk(0x20, '\x7F\x12\x80')
        chunk.write(buffer)

        assert buffer.getvalue() == '\x7F\x12\x80'

    def test_split(self):
        chunk = GmeRawChunk(0x20, 'ABCDEFGHIJKL')
        (head, tail) = chunk.split('raw', 2, 'raw')

        assert head.__class__.__name__ == 'GmeRawChunk'
        assert head.offset == 0x20
        assert head.buffer == 'AB'
        assert tail.__class__.__name__ == 'GmeRawChunk'
        assert tail.offset == 0x22
        assert tail.buffer == 'CDEFGHIJKL'

    def test_split_empty_start(self):
        chunk = GmeRawChunk(0x20, 'ABCDEFGHIJKL')
        (head, tail) = chunk.split('raw', 0, 'raw')

        assert head.__class__.__name__ == 'GmeRawChunk'
        assert head.offset == 0x20
        assert head.buffer == ''
        assert tail.__class__.__name__ == 'GmeRawChunk'
        assert tail.offset == 0x20
        assert tail.buffer == 'ABCDEFGHIJKL'

    def test_split_empty_end(self):
        chunk = GmeRawChunk(0x20, 'ABCDEFGHIJKL')
        (head, tail) = chunk.split('raw', 12, 'raw')

        assert head.__class__.__name__ == 'GmeRawChunk'
        assert head.offset == 0x20
        assert head.buffer == 'ABCDEFGHIJKL'
        assert tail.__class__.__name__ == 'GmeRawChunk'
        assert tail.offset == 0x2C
        assert tail.buffer == ''

    def test_split_after_end(self):
        chunk = GmeRawChunk(0x20, 'ABCD')
        with self.assertRaises(RuntimeError) as context:
            chunk.split('raw', 5, 'raw')
        assert 'past end' in str(context.exception)

    def test_split_before_start_end(self):
        chunk = GmeRawChunk(0x20, 'ABCD')
        with self.assertRaises(RuntimeError) as context:
            chunk.split('raw', -5, 'raw')
        assert 'before start' in str(context.exception)

    def test_split_negative_offset(self):
        chunk = GmeRawChunk(0x20, 'ABCDEFGHIJKL')
        (head, tail) = chunk.split('raw', -4, 'raw')

        assert head.__class__.__name__ == 'GmeRawChunk'
        assert head.offset == 0x20
        assert head.buffer == 'ABCDEFGH'
        assert tail.__class__.__name__ == 'GmeRawChunk'
        assert tail.offset == 0x28
        assert tail.buffer == 'IJKL'

    def test_split_left_checksum(self):
        chunk = GmeRawChunk(0x20, 'AB\x01\x02\x03\x04')
        (head, tail) = chunk.split('checksum', 4, 'raw')

        assert head.__class__.__name__ == 'GmeChecksumChunk'
        assert head.offset == 0x20
        assert head.buffer == 'AB\x01\x02'
        assert tail.__class__.__name__ == 'GmeRawChunk'
        assert tail.offset == 0x24
        assert tail.buffer == '\x03\x04'

    def test_split_right_checksum(self):
        chunk = GmeRawChunk(0x20, 'AB\x01\x02\x03\x04')
        (head, tail) = chunk.split('raw', 2, 'checksum')

        assert head.__class__.__name__ == 'GmeRawChunk'
        assert head.offset == 0x20
        assert head.buffer == 'AB'
        assert tail.__class__.__name__ == 'GmeChecksumChunk'
        assert tail.offset == 0x22
        assert tail.buffer == '\x01\x02\x03\x04'

    def test_explain(self):
        chunk = GmeRawChunk(0x21, 'ABCDEF')
        explanation = chunk.explain()
        assert 'GmeRawChunk' in explanation
        assert '00000020:  -- 41 42 43 44 45 46 --' in explanation

    def test_format_byte_too_low_offset(self):
        chunk = GmeRawChunk(0x20, '\x12')
        assert chunk.format_byte(0x18) == '--'

    def test_format_byte_too_high_offset(self):
        chunk = GmeRawChunk(0x20, '\x12')
        assert chunk.format_byte(0x18) == '--'

    def test_format_byte_04(self):
        chunk = GmeRawChunk(0x20, '\x04')
        assert chunk.format_byte(0x20) == '04'

    def test_format_byte_12(self):
        chunk = GmeRawChunk(0x20, '\x12')
        assert chunk.format_byte(0x20) == '12'

    def test_format_byte_in_bigger_buffer(self):
        chunk = GmeRawChunk(0x20, '\x04\x12\x06')
        assert chunk.format_byte(0x21) == '12'

    def test_format_buffer_full_line(self):
        chunk = GmeRawChunk(0x20, 'ABCDEFGHIJKLMNOP')
        assert chunk.format_buffer() == \
            '00000020:  41 42 43 44 45 46 47 48  49 4A 4B 4C 4D 4E 4F 50\n'

    def test_format_buffer_uneven_start(self):
        chunk = GmeRawChunk(0x21, 'BCDABCDABCDABCD')
        assert chunk.format_buffer() == \
            '00000020:  -- 42 43 44 41 42 43 44  41 42 43 44 41 42 43 44\n'

    def test_format_buffer_uneven_end(self):
        chunk = GmeRawChunk(0x20, 'ABCDABCDABCDABC')
        assert chunk.format_buffer() == \
            '00000020:  41 42 43 44 41 42 43 44  41 42 43 44 41 42 43 --\n'

    def test_format_buffer_uneven_start_and_end(self):
        chunk = GmeRawChunk(0x22, 'CDABCDABCDA')
        assert chunk.format_buffer() == \
            '00000020:  -- -- 43 44 41 42 43 44  41 42 43 44 41 -- -- --\n'

    def test_format_buffer_three_lines(self):
        chunk = GmeRawChunk(0x1234561e, 'EFABCDABCDABCDABCD012')
        assert chunk.format_buffer() == (
            '12345610:  -- -- -- -- -- -- -- --  -- -- -- -- -- -- 45 46\n'
            + '12345620:  41 42 43 44 41 42 43 44  41 42 43 44 41 42 43 44\n'
            + '12345630:  30 31 32 -- -- -- -- --  -- -- -- -- -- -- -- --\n'
            )
