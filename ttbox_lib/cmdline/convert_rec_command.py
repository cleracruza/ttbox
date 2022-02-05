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

The WAV file gets written to REC file's name with ".wav" appended.

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
        return ''.join([chr(ord(x) ^ 0x6a) for x in buffer])

    def write_wav(self, buffer):
        with open(self.REC_FILE + '.wav', 'wb') as f:
            f.write(buffer)

    def run(self):
        buffer = self.read_rec()

        buffer = self.convert_to_wav(buffer)

        self.write_wav(buffer)
