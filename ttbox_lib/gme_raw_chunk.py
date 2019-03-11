import sys
from struct import pack


class GmeRawChunk(object):
    def __init__(self, offset, buffer):
        self.offset = offset
        self.buffer = buffer
        self.length = len(self.buffer)

    def kind_to_cls(self, kind):
        module = 'ttbox_lib.gme_' + kind + '_chunk'
        name = 'Gme' + kind[0].upper() + kind[1:] + 'Chunk'
        return getattr(sys.modules[module], name)

    def set_int32(self, offset, value):
        size = 4
        if size > self.length:
            raise RuntimeError(('Setting %d bytes is beyond the chunk size '
                                + '(%d)') % (size, self.length))
        if offset + size > self.length:
            raise RuntimeError(('Setting value at offset %d would run past '
                                + 'chunk end') % (offset))
        if offset < -self.length:
            raise RuntimeError(('Setting value at offset %d would be before '
                                + 'chunk start') % (offset))
        if offset < 0:
            offset += self.length

        self.buffer = self.buffer[0:offset] + pack('<I', value) \
            + self.buffer[offset + size:]

    def checksum(self):
        ret = 0
        for b in self.buffer:
            ret += ord(b)
        return ret & 0xffffffff

    def write(self, f):
        f.write(self.buffer)

    def split(self, head_kind, offset, tail_kind):
        head_cls = self.kind_to_cls(head_kind)
        tail_cls = self.kind_to_cls(tail_kind)
        if offset > self.length:
            raise RuntimeError(('Splitting chunk of size %s past end (at '
                                + 'position %d) is not supported') % (
                    self.length, offset))
        if offset < -self.length:
            raise RuntimeError(('Splitting chunk of size %s before start (at '
                                + 'position %d) is not supported') % (
                    self.length, offset))
        if offset < 0:
            offset += self.length
        head = head_cls(self.offset, self.buffer[0:offset])
        tail = tail_cls(self.offset + offset, self.buffer[offset:])
        return (head, tail)

    def explain(self):
        return '\n%s\n%s\n' % (str(self), self.format_buffer())

    def format_byte(self, offset):
        ret = '--'
        if self.offset <= offset and offset < self.offset + self.length:
            byte = ord(self.buffer[offset - self.offset])
            ret = '%.02X' % (byte)

        return ret

    def format_buffer(self):
        start = (self.offset & 0xfffffff0)
        end = ((self.offset + self.length - 1) & 0xfffffff0) + 0x0f

        line = start
        ret = ''
        while line < end:
            ret += ('%.08X:  %s %s %s %s %s %s %s %s '
                    + ' %s %s %s %s %s %s %s %s\n') % (
                line,
                self.format_byte(line + 0), self.format_byte(line + 1),
                self.format_byte(line + 2), self.format_byte(line + 3),
                self.format_byte(line + 4), self.format_byte(line + 5),
                self.format_byte(line + 6), self.format_byte(line + 7),
                self.format_byte(line + 8), self.format_byte(line + 9),
                self.format_byte(line + 10), self.format_byte(line + 11),
                self.format_byte(line + 12), self.format_byte(line + 13),
                self.format_byte(line + 14), self.format_byte(line + 15),
                )
            line += 16

        return ret

    def __str__(self):
        return "%s(offset: %d, len: %d)" % (self.__class__.__name__,
                                            self.offset, self.length)
