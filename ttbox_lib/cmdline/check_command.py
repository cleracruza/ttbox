import sys


from . import GmeCommand, warn


class CheckCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'check a GME file for obvious errors'

    def get_subparser_description(self):
        return 'Currently, this commands only checks the checksum.'

    def run(self):
        issues = self.gme.check()
        exit_code = 1
        if issues:
            for issue in issues:
                warn(issue)
            print "File has at least %d issues." % (len(issues))
            exit_code = 1
        else:
            print "File is ok."
            exit_code = 0
        sys.exit(exit_code)
