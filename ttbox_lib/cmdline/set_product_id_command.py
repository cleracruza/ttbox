from . import GmeCommand


class SetProductIdCommand(GmeCommand):
    def get_subparser_short_help(self):
        return 'sets the product id of a GME file'

    def configure(self, config, args):
        super(SetProductIdCommand, self).configure(config, args)
        self.product_id = args.PRODUCT_ID

    def register_subparser(self, subparsers):
        parser = super(SetProductIdCommand, self).register_subparser(
            subparsers)

        parser.add_argument('PRODUCT_ID',
                            type=int,
                            help='The product id to set')

    def run(self):
        self.gme.set_product_id(self.product_id)
        self.gme.write(self.GME_FILE)
