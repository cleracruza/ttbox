from . import GmeCommand


class ClearLanguageCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'clears the language setting of a GME file'

    def get_subparser_description(self):
        return 'Some GME files come with language restrictions (E.g.: can ' + \
            'only be played by pens that are set to French). By clearing ' + \
            'the GME file\'s language setting, such restrictions are ' + \
            'dropped and the GME file can be played on pens regardless of ' + \
            'their set language.'

    def run(self):
        self.gme.set_language('')
        self.gme.write(self.GME_FILE)
