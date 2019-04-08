SVG_WITHOUT_OIDS_FILES=$(shell find -iname '*.svg' ! -iname '*-with-oids.svg' )

TTBOX="ttbox/ttbox"

YAML_FILE=$(shell find \( -name ttbox -prune \) -o \( -name .git -prune \) -o \( -iname '*.yaml' ! -iname '*.codes.yaml' -print \) | sort | head -n 1)
GME_FILE=$(YAML_FILE:%.yaml=%.gme)
SVG_WITH_OIDS_FILES=$(SVG_WITHOUT_OIDS_FILES:%.svg=%-with-oids.svg)

PNG_WITHOUT_OIDS_FILES=$(SVG_WITHOUT_OIDS_FILES:%.svg=%.png)
PNG_WITH_OIDS_FILES=$(SVG_WITH_OIDS_FILES:%.svg=%.png)

PDF_WITHOUT_OIDS_FILES=$(SVG_WITHOUT_OIDS_FILES:%.svg=%.pdf)
PDF_WITH_OIDS_FILES=$(SVG_WITH_OIDS_FILES:%.svg=%.pdf)

PRODUCT_ID=$(shell ${TTBOX} print-product-id ${YAML_FILE})
OIDS=$(shell ${TTBOX} print-oids ${YAML_FILE})
CODE_YAML_FILE=$(shell ${TTBOX} print-codes-yaml ${YAML_FILE})
TTTOOL_OID_FILES=$(OIDS:%=oid-$(PRODUCT_ID)-%.png)
EXTRACTED_OID_FILES=$(TTTOOL_OID_FILES:%.png=%-extracted.png)

all:: $(GME_FILE) $(SVG_WITH_OIDS_FILES) $(EXTRACTED_OID_FILES)

clean::
	rm -f $(GME_FILE) \
		$(SVG_WITH_OIDS_FILES) \
		$(PNG_WITH_OIDS_FILES) $(PNG_WITHOUT_OIDS_FILES) \
		$(PDF_WITH_OIDS_FILES) $(PDF_WITHOUT_OIDS_FILES) \
		$(TTTOOL_OID_FILES) $(EXTRACTED_OID_FILES)

test:: all

check: test

pngs-with-oids:: $(PNG_WITH_OIDS_FILES)
pngs-without-oids:: $(PNG_WITHOUT_OIDS_FILES)
pngs: pngs-with-oids pngs-without-oids

pdfs-with-oids:: $(PDF_WITH_OIDS_FILES)
pdfs-without-oids:: $(PDF_WITHOUT_OIDS_FILES)
pdfs: pdfs-with-oids pdfs-without-oids

full-monty: all pngs pdfs check

$(TTTOOL_OID_FILES): $(YAML_FILE) $(CODE_YAML_FILE)
# We generate only a small patch of the OID to keep file sizes small,
# and SVG's automatic pattern tiling is used to get the OIDs onto
# bigger objects.
# As an OID is 48 pixels at 1200, which is 1.016mm and hence bigger
# than 1mm, we use code-dim of 2. This of course means that we
# generate about 2x2 OID codes, which we later (see `-extracted` rule) have
# to extract out again.
	tttool --code-dim 2 oid-codes $<

$(GME_FILE): $(YAML_FILE) $(CODE_YAML_FILE)
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

%.png: %.svg $(EXTRACTED_OID_FILES)
	inkscape \
		--export-dpi=1200 \
		--export-png=$@ \
		$<

# When converting SVGs directly to PDFs using inkscape, the OIDs do
# not show up when rendering the PDFs with gimp. So we convert to PDF
# from PNG.
%.pdf: %.png
	convert $< -density 1200 -set units PixelsPerInch $@
