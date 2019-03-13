class BaseCommand(object):
    def __init__(self):
        pass

    def configure(self, config, args):
        pass

    def get_subparser_short_help(self):
        raise NotImplementedError(
            'Please implement this fuction in your subclass')

    def register_subparser(self, subparsers):
        command_name = self.__class__.__name__
        if command_name.endswith('Command'):
            command_name = command_name[0:-7]
        command_name = ''.join([
                (letter if letter.islower() else ('-' + letter))
                for letter in command_name])[1:]
        command_name = command_name.lower()

        parser = subparsers.add_parser(command_name,
                                       help=self.get_subparser_short_help())

        parser.set_defaults(command=self)

        return parser

    def __str__(self):
        raise NotImplementedError(
            'Please implement this fuction in your subclass')

    def run(self):
        raise NotImplementedError(
            'Please implement this fuction in your subclass')
