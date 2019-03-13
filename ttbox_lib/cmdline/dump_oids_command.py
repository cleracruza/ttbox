from . import YamlCommand


class DumpOidsCommand(YamlCommand):
    def get_subparser_short_help(self):
        return 'print the oids of a YAML file'

    def get_subparser_description(self):
        return 'The set of OIDs includes the START OID.\n\n' + \
            'Each OID is printed on a separate line.'

    def run(self):
        oids = sorted(self.yaml.get('scripts', {}).keys() + ['START'])
        print("\n".join(oids))
