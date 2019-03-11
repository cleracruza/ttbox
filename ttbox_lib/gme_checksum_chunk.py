from struct import unpack
from . import GmeRawChunk


class GmeChecksumChunk(GmeRawChunk):
    def __str__(self):
        ret = super(GmeChecksumChunk, self).__str__()
        ret += "(checksum: %s)" % (unpack('<I', self.buffer))
        return ret
