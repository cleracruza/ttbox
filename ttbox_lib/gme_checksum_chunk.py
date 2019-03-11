from struct import unpack
from . import GmeRawChunk


class GmeChecksumChunk(GmeRawChunk):
    def __init__(self, offset, buffer):
        super(GmeChecksumChunk, self).__init__(offset, buffer)
        if self.length != 4:
            raise RuntimeError('Checksum chunk has to have length 4, but has '
                               + '%d.' % (self.length))

    def __str__(self):
        ret = super(GmeChecksumChunk, self).__str__()
        ret += "(checksum: %s)" % (unpack('<I', self.buffer))
        return ret
