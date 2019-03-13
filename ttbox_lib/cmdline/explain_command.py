from . import GmeCommand


class ExplainCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'print an annotated dump of the GME file'

    def run(self):
        print(self.gme.explain())
