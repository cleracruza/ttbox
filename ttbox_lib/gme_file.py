from struct import pack
from . import GmeRawChunk


class GmeFile(object):
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, 'rb') as f:
            buffer = f.read()
        full = GmeRawChunk(0, buffer)

        (full_no_checksum, checksum) = full.split('raw', -4, 'checksum')

        self.chunks = [full_no_checksum, checksum]

    def set_product_id(self, product_id):
        header = self.chunks[0]
        header.setInt32(0x14, product_id)

    def checksum(self):
        ret = 0
        for chunk in self.chunks[:-1]:
            ret += chunk.checksum()
        return ret & 0xffffffff

    def write(self, file_name):
        with open(file_name, 'wb') as f:
            for chunk in self.chunks[:-1]:
                chunk.write(f)
            f.write(pack('<I', self.checksum()))
