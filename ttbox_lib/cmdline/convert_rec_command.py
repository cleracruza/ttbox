import os
import subprocess
import sys

from . import BaseCommand


LAME_BINARY = os.path.join('/usr', 'bin', 'lame')


class ConvertRecCommand(BaseCommand):
    def configure(self, config, args):
        self.REC_FILE = args.REC_FILE
        self.OUTPUT_FILE = args.OUTPUT_FILE
        self.format = args.format[0]

    def get_subparser_short_help(self):
        return 'converts a REC file to a WAV/MP3 file'

    def get_subparser_description(self):
        return '''\
This command converts a REC file (i.e.: the files that pens store their
recordings in) to a WAV/MP3 file.

This is useful to backup your pen's recordings and archive them in a commonly
used format.
'''

    def register_subparser(self, subparsers):
        parser = super(ConvertRecCommand, self).register_subparser(
            subparsers)

        parser.add_argument('REC_FILE',
                            help='REC file to convert')

        parser.add_argument(
            'OUTPUT_FILE', nargs='?', help='File name to write the WAV file '
            'to. If empty or not provded, it defaults to the REC_FILE with '
            'trailing ".rec" removed and "." and the output file format '
            'appended. Use - to write to ' 'stdout.', default='')

        parser.add_argument(
            '--format', choices=['wav', 'mp3'], nargs=1, help='The format to '
            'convert the REC file to. "wav" converts to plain, uncompressed, '
            'lossless wav. "mp3" uses "lame" to convert to mp3.',
            default=['wav'])

        return parser

    def read_rec(self):
        with open(self.REC_FILE, 'rb') as f:
            return f.read()

    def convert_to_wav(self, buffer):
        # The magic XOR value 0x6a is from
        # https://github.com/entropia/tip-toi-reveng/wiki/REC-file-format#the-file-format
        return ''.join([chr(ord(x) ^ 0x6a) for x in buffer])

    def convert_to_mp3(self, buffer):
        if not os.path.isfile(LAME_BINARY):
            raise RuntimeError('lame binary not found at %s' % LAME_BINARY)
        p = subprocess.Popen(
            [LAME_BINARY, '-', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate(buffer)
        if p.returncode:
            raise RuntimeError('Running lame failed with return code %d: %s' %
                               (p.returncode, stderr))
        return stdout

    def write_wav(self, buffer):
        target = self.OUTPUT_FILE
        if not target:
            target = self.REC_FILE
            if target.endswith('.rec'):
                target = target[:-4]
            target += '.' + self.format

        if target == '-':
            sys.stdout.write(buffer)
        else:
            with open(target, 'wb') as f:
                f.write(buffer)

    def run(self):
        buffer = self.read_rec()

        buffer = self.convert_to_wav(buffer)

        if self.format == 'wav':
            # Nothing to do. Buffer is already in wav format
            pass
        elif self.format == 'mp3':
            buffer = self.convert_to_mp3(buffer)
        else:
            raise RuntimeError('Unsupported format ' % (self.format))

        self.write_wav(buffer)
