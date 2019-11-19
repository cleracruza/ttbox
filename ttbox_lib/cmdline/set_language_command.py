from . import GmeCommand


class SetLanguageCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'set the language of a GME file'

    def get_subparser_description(self):
        return 'If the language of a GME file is not empty and does not ' + \
            'match the pen\'s language, the pen will refuse to play it. ' + \
            'So for example you cannot play a French GME file using a pen ' + \
            'set to German. This command allows you to adjust a GME ' + \
            'file\'s language to match the pen\'s language, so you can ' + \
            'play the GME file.'

    def configure(self, config, args):
        super(SetLanguageCommand, self).configure(config, args)
        self.language = args.LANGUAGE

    def register_subparser(self, subparsers):
        parser = super(SetLanguageCommand, self).register_subparser(
            subparsers)

        parser.add_argument('LANGUAGE',
                            help='The language to set (Typically upper-case ' +
                            'English name of the language. E.g. GERMAN, ' +
                            'FRENCH)')

    def run(self):
        self.gme.set_language(self.language)
        self.gme.write(self.GME_FILE)
