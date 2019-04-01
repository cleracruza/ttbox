CODE_YAML_FILE=$(shell find -iname '*.codes.yaml')
SVG_WITHOUT_OIDS_FILES=$(shell find -iname '*.svg' ! -iname '*-with-oids.svg' )

TTBOX="ttbox/ttbox"

YAML_FILE=$(CODE_YAML_FILE:%.codes.yaml=%.yaml)
GME_FILE=$(YAML_FILE:%.yaml=%.gme)
SVG_WITH_OIDS_FILES=$(SVG_WITHOUT_OIDS_FILES:%.svg=%-with-oids.svg)

PRODUCT_ID=$(shell ${TTBOX} print-product-id ${YAML_FILE})
OIDS=$(shell ${TTBOX} print-oids ${YAML_FILE})
TTTOOL_OID_FILES=$(OIDS:%=oid-$(PRODUCT_ID)-%.png)
EXTRACTED_OID_FILES=$(TTTOOL_OID_FILES:%.png=%-extracted.png)

all:: $(GME_FILE) $(SVG_WITH_OIDS_FILES) $(EXTRACTED_OID_FILES)

clean::
	rm -f $(GME_FILE) $(SVG_WITH_OIDS_FILES) $(TTTOOL_OID_FILES) $(EXTRACTED_OID_FILES)

$(TTTOOL_OID_FILES): $(YAML_FILE) $(CODE_YAML_FILE)
# We generate only a small patch of the OID to keep file sizes small,
# and SVG's automatic pattern tiling is used to get the OIDs onto
# bigger objects.
# As an OID is 48 pixels at 1200, which is 1.016mm and hence bigger
# than 1mm, we use code-dim of 2. This of course means that we
# generate about 2x2 OID codes, which we later (see `-extracted` rule) have
# to extract out again.
	tttool --code-dim 2 oid-codes $<

%.gme: %.yaml %.codes.yaml
	tttool assemble $<

%-extracted.png: %.png
# See rule for oid files above on why we shave of from the original OID.
	convert -shave 23x23 $< $@

%-with-oids.svg: %.svg
	xsltproc \
		--stringparam productId $(PRODUCT_ID) \
		--stringparam oidSize 1.016mm \
		--stringparam oidSuffix -extracted \
		- $< <ttbox/svg-oid-insertion.xsl >$@

%-with-oids.svg: %-generated.svg
	xsltproc \
		--stringparam productId $(PRODUCT_ID) \
		--stringparam oidSize 1.016mm \
		--stringparam oidSuffix -extracted \
		- $< <ttbox/svg-oid-insertion.xsl >$@
