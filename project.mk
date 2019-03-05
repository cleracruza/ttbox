CODE_YAML_FILE=$(shell find -iname '*.codes.yaml')
SVG_WITHOUT_OIDS_FILES=$(shell find -iname '*.svg' ! -iname '*-with-oids.svg' )

YAML_DUMP="ttbox/yaml-dump"

YAML_FILE=$(CODE_YAML_FILE:%.codes.yaml=%.yaml)
GME_FILE=$(YAML_FILE:%.yaml=%.gme)
SVG_WITH_OIDS_FILES=$(SVG_WITHOUT_OIDS_FILES:%.svg=%-with-oids.svg)

PRODUCT_ID=$(shell ${YAML_DUMP} PRODUCT-ID ${YAML_FILE})
OIDS=$(shell ${YAML_DUMP} OIDS ${YAML_FILE})
TTTOOL_OID_FILES=$(OIDS:%=oid-$(PRODUCT_ID)-%.png)
EXTRACTED_OID_FILES=$(TTTOOL_OID_FILES:%.png=%-extracted.png)

all: $(GME_FILE) $(SVG_WITH_OIDS_FILES) $(EXTRACTED_OID_FILES)

foo:
	echo $(OIDS)
	echo $(TTTOOL_OID_FILES)

clean:
	rm -f $(GME_FILE) $(SVG_WITH_OIDS_FILES) $(TTTOOL_OID_FILES) $(EXTRACTED_OID_FILES)

$(TTTOOL_OID_FILES): $(YAML_FILE) $(CODE_YAML_FILE)
	tttool --code-dim 2 oid-codes $<

%.gme: %.yaml %.codes.yaml media/*
	tttool assemble $<

%-extracted.png: %.png
	convert -extract 48x48+10+10 $< $@

%-with-oids.svg: %.svg
	xsltproc \
		--stringparam productId $(PRODUCT_ID) \
		--stringparam oidSize 1.016mm \
		--stringparam oidSuffix -extracted \
		- $< <ttbox/svg-oid-insertion.xsl >$@
