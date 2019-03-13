from . import BaseCommand
from .. import GmeFile


class GmeCommand(BaseCommand):
    def configure(self, config, args):
        self.GME_FILE = args.GME_FILE
        self.gme = self.getGme(self.GME_FILE)

    def register_subparser(self, subparsers):
        parser = super(GmeCommand, self).register_subparser(
            subparsers)

        parser.add_argument('GME_FILE',
                            help='GME file to parse')

        return parser

    def getGme(self, gme_file):
        return GmeFile(gme_file)
