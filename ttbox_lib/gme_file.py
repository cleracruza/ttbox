from struct import pack
from . import GmeRawChunk


class GmeFile(object):
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'rb') as f:
            buffer = f.read()
        rest = GmeRawChunk(0, buffer)
        (rest, checksum) = rest.split('raw', -4, 'checksum')

        self.chunks = [rest, checksum]

    def set_product_id(self, product_id):
        header = self.chunks[0]
        header.setInt32(0x14, product_id)

    def checksum(self):
        ret = 0
        for chunk in self.chunks[:-1]:
            ret += chunk.checksum()
        return ret & 0xffffffff

    def explain(self):
        return ''.join([chunk.explain() for chunk in self.chunks])

    def write(self, file_name):
        with open(file_name, 'wb') as f:
            for chunk in self.chunks[:-1]:
                chunk.write(f)
            f.write(pack('<I', self.checksum()))
