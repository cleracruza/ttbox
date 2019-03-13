from . import YamlCommand


class DumpOidsCommand(YamlCommand):
    def get_subparser_short_help(self):
        return 'print the oids of a YAML file'

    def run(self):
        oids = sorted(self.yaml.get('scripts', {}).keys() + ['START'])
        print("\n".join(oids))
