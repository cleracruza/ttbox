from . import GmeCommand


class UpdateChecksumCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'updates the checksum stored in a GME file'

    def run(self):
        self.gme.write(self.GME_FILE)
