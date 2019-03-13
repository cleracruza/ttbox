from . import YamlCommand


class PrintProductIdCommand(YamlCommand):
    def get_subparser_short_help(self):
        return 'print the product id of a YAML file'

    def run(self):
        print(self.yaml.get('product-id', None))
