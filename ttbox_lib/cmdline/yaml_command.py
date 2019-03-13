import yaml

from . import BaseCommand, error


class YamlCommand(BaseCommand):
    def configure(self, config, args):
        self.YAML_FILE = args.YAML_FILE
        self.yaml = self.getYaml(self.YAML_FILE)

    def register_subparser(self, subparsers):
        parser = super(YamlCommand, self).register_subparser(
            subparsers)

        parser.add_argument('YAML_FILE',
                            help='YAML file to parse')

        return parser

    def getYaml(self, yaml_file):
        with open(yaml_file, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                error(str(exc))
