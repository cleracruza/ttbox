from . import GmeCommand


class UpdateChecksumCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'update the checksum stored in a GME file'

    def run(self):
        self.gme.write(self.GME_FILE)
