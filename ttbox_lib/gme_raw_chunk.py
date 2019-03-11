import sys
from struct import pack


class GmeRawChunk(object):
    def __init__(self, offset, buffer):
        self.offset = offset
        self.buffer = buffer

    def kind_to_cls(self, kind):
        module = 'ttbox_lib.gme_' + kind + '_chunk'
        name = 'Gme' + kind[0].upper() + kind[1:] + 'Chunk'
        return getattr(sys.modules[module], name)

    def setInt32(self, offset, value):
        self.buffer = self.buffer[0:offset] + pack('<I', value) \
            + self.buffer[offset+4:]

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
        if (offset < len(self.buffer)):
            offset += len(self.buffer)
        head = head_cls(0, self.buffer[0:offset])
        tail = tail_cls(offset, self.buffer[offset:])
        return (head, tail)

    def __str__(self):
        return "%s(offset: %d, len: %d)" % (self.__class__.__name__,
                                            self.offset, len(self.buffer))
