from . import BaseCommand


class ConvertRecCommand(BaseCommand):
    def configure(self, config, args):
        self.REC_FILE = args.REC_FILE

    def get_subparser_short_help(self):
        return 'converts a REC file to WAV file'

    def get_subparser_description(self):
        return '''\
This command converts a REC file (i.e.: the files that pens store their
recordings in) to a WAV file.

The WAV file gets written to REC file's name with an eventual ".rec" stripped
and ".wav" appended.

This is useful to backup your pen's recordings and archive them in a commonly
used format.
'''

    def register_subparser(self, subparsers):
        parser = super(ConvertRecCommand, self).register_subparser(
            subparsers)

        parser.add_argument('REC_FILE',
                            help='REC file to convert')

        return parser

    def read_rec(self):
        with open(self.REC_FILE, 'rb') as f:
            return f.read()

    def convert_to_wav(self, buffer):
        # The magic XOR value 0x6a is from
        # https://github.com/entropia/tip-toi-reveng/wiki/REC-file-format#the-file-format
        return ''.join([chr(ord(x) ^ 0x6a) for x in buffer])

    def write_wav(self, buffer):
        target = self.REC_FILE
        if target.endswith('.rec'):
            target = target[:-4]
        target += '.wav'

        with open(target, 'wb') as f:
            f.write(buffer)

    def run(self):
        buffer = self.read_rec()

        buffer = self.convert_to_wav(buffer)

        self.write_wav(buffer)
