from ttbox_lib import GmeRawChunk


class TestGmeRawChunk():
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
