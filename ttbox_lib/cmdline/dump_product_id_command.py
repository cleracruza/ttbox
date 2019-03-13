from . import YamlCommand


class DumpProductIdCommand(YamlCommand):
    def get_subparser_short_help(self):
        return 'prints the product id of a YAML file'

    def run(self):
        print(self.yaml.get('product-id', None))
