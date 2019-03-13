import sys


def error(msg):
    sys.stderr.write("ERROR: %s\n" % (msg))
    sys.exit(1)


def warn(msg):
    sys.stderr.write("WARN: %s\n" % (msg))
