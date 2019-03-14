# ttbox

Toolbox for working with files for [TipToi](https://www.tiptoi.com/) pens.

* [Installation](#installation)
* [OID insertion in SVGs](#oid-insertion-in-svgs)
* [GME/YAML tooling](#gmeyaml-tooling)
* [Acknowledgements](#acknowledgements)
* [Questions/Support](#questionssupport)

[![Build Status](https://travis-ci.org/cleracruza/ttbox.svg?branch=master)](https://travis-ci.org/cleracruza/ttbox)

## Installation

* Install [`tttool`](https://github.com/entropia/tip-toi-reveng), GNU Make, Python, PyYAML, and ImageMagick.
* Clone this repository
```
git clone https://github.com/cleracruza/ttbox.git
```
* Done. ttbox is ready to use.

## OID insertion in SVGs

Given an SVG that has some elements tagged with OID names (e.g.: using [Inkscape](https://inkscape.org/)), `ttbox` can automatically insert the OID codes to the tagged elements and prepare the SVG for TipToi usage. It requires some care when generating the original SVGs, but saves a ton of time afterwards, as one can re-align/add/remove/... SVG elements without having to manually (and time-consumingly!) redo the OIDs.

See [svg-oid-insertion.md](svg-oid-insertion.md) for details.

## GME/YAML tooling

The `ttbox` script allows to modify or extract information from GME/YAML files.

`./ttbox --help` gives a brief overview over the available commands:

```
$ ./ttbox --help
usage: ttbox [-h]
             
             {check,explain,print-oids,print-product-id,set-product-id,update-checksum}
             ...

Toolbox for GME and tttool yaml files

optional arguments:
  -h, --help            show this help message and exit

Commands:
  Available commands

  {check,explain,print-oids,print-product-id,set-product-id,update-checksum}
    check               check a GME file for obvious errors
    explain             print an annotated dump of the GME file
    print-oids          print the oids of a YAML file
    print-product-id    print the product id of a YAML file
    set-product-id      set the product id of a GME file
    update-checksum     update the checksum stored in a GME file
```

Invoking one of the commands with `--help` gives a more detailed description of the command. For example

```
$ ./ttbox print-oids --help
usage: ttbox print-oids [-h] YAML_FILE

Print the oids of a YAML file.

The set of OIDs includes the START OID.

Each OID is printed on a separate line.

positional arguments:
  YAML_FILE   YAML file to parse

optional arguments:
  -h, --help  show this help message and exit
```

## Acknowledgements

ttbox is based on [tttool (tip-toi-reveng)](https://github.com/entropia/tip-toi-reveng) and the [fantastic community](https://lists.nomeata.de/mailman/listinfo/tiptoi) around it that [reversed the GME file format](https://github.com/entropia/tip-toi-reveng/blob/master/GME-Format.md).

## Questions/Support

If you run into issues or have questions, please file a ticket at [GitHub's issue tracker](https://github.com/cleracruza/ttbox/issues/new)
