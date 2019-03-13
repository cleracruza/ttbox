from . import GmeCommand


class UpdateChecksumCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'update the checksum stored in a GME file'

    def get_subparser_description(self):
        return '''\
This command re-computes the GME file's checksum and stores it in the
file.

This is especially useful to get a valid GME file and having edited a
GME file by hand.
'''

    def run(self):
        self.gme.write(self.GME_FILE)
