from . import YamlCommand
from os import access, R_OK
from os.path import isfile


class PrintCodesYamlCommand(YamlCommand):
    def get_subparser_short_help(self):
        return 'print the name of the file holding scriptcodes'

    def run(self):
        file = None
        if 'scriptcodes' in self.yaml:
            file = self.YAML_FILE
        elif self.YAML_FILE.endswith('.yaml'):
            (start, end) = self.YAML_FILE.rsplit('.', 1)
            codes_file_name = start + '.codes.' + end
            if isfile(codes_file_name) and access(codes_file_name, R_OK):
                codes_yaml = self.getYaml(codes_file_name)
                if 'scriptcodes' in codes_yaml:
                    file = codes_file_name
                else:
                    raise RuntimeError("Failed to find 'scriptcodes' key in "
                                       "both '%s' and '%s'" %
                                       (self.YAML_FILE, codes_file_name))
            else:
                raise RuntimeError("'%s' is not a readable file and failed to "
                                   "find 'scriptcodes' key in '%s' " %
                                   (codes_file_name, self.YAML_FILE))
        else:
            raise RuntimeError("Name of YAML file '%s' does not end in "
                               "'.yaml'. Hence, I cannot construct the "
                               "'.codes.yaml' file name" %
                               (self.YAML_FILE))
        print file
