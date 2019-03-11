from . import GmeRawChunk


class GmeChecksumChunk(GmeRawChunk):
    def __init__(self, offset, buffer):
        super(GmeChecksumChunk, self).__init__(offset, buffer)
        if self.length != 4:
            raise RuntimeError('Checksum chunk has to have length 4, but has '
                               + '%d.' % (self.length))

    def stored_checksum(self):
        return self.get_int32(0)

    def __str__(self):
        ret = super(GmeChecksumChunk, self).__str__()
        ret += "(checksum: %s)" % (self.stored_checksum())
        return ret
