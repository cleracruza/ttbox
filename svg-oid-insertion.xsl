<?xml version="1.0"?>
<xsl:stylesheet version = "1.0" 
                xmlns:cc="http://creativecommons.org/ns#"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                xmlns:svg="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:xsl = "http://www.w3.org/1999/XSL/Transform"
                >

<xsl:param name="productId" select="&quot;900&quot;"/>
<xsl:param name="oidSize" select="&quot;30mm&quot;"/>
<xsl:param name="oidSuffix"/>
<xsl:param name="needs-start-button" select="contains(/svg:svg/svg:metadata[1]/rdf:RDF[1]/cc:Work[1]/dc:subject[1],&quot;(ttbox-start-button)&quot;)"/>

<xsl:template match="@style" mode="restyle">
        <xsl:attribute name="style">fill:url(#pattern-oid-<xsl:value-of select="substring-before(substring-after(string(../svg:desc[1]),&quot;(oid:&quot;), &quot;&#41;&quot;)"/>);fill-opacity:1.0</xsl:attribute>
</xsl:template>

<xsl:template match="@id">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
</xsl:template>

<xsl:template match="@id" mode="restyle"></xsl:template>


<xsl:template match="//*[contains(string(svg:desc[1]), &quot;oid&quot;)]" mode="restyle">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*" mode="restyle"/>
    </xsl:copy>
</xsl:template>

<xsl:template match="svg:defs[1]">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
        <xsl:for-each select="//*[contains(string(svg:desc[1]), &quot;oid&quot;)]">
            <svg:pattern>
                <xsl:attribute name="id">pattern-oid-<xsl:value-of select="substring-before(substring-after(string(.),&quot;(oid:&quot;), &quot;&#41;&quot;)"/></xsl:attribute>
                <xsl:attribute name="width"><xsl:value-of select="$oidSize"/></xsl:attribute>
                <xsl:attribute name="height"><xsl:value-of select="$oidSize"/></xsl:attribute>
                <xsl:attribute name="patternTransform">translate(0,0)</xsl:attribute>
                <xsl:attribute name="patternUnits">userSpaceOnUse</xsl:attribute>
                <svg:image x="0" y="0">
                    <xsl:attribute name="width"><xsl:value-of select="$oidSize"/></xsl:attribute>
                    <xsl:attribute name="height"><xsl:value-of select="$oidSize"/></xsl:attribute>
                    <xsl:attribute name="xlink:href">./oid-<xsl:value-of select="$productId"/>-<xsl:value-of select="substring-before(substring-after(string(.),&quot;(oid:&quot;), &quot;&#41;&quot;)"/><xsl:value-of select="$oidSuffix"/>.png</xsl:attribute>
                </svg:image>
            </svg:pattern>
        </xsl:for-each>
        <svg:pattern>
            <xsl:attribute name="id">pattern-oid-START</xsl:attribute>
            <xsl:attribute name="width"><xsl:value-of select="$oidSize"/></xsl:attribute>
            <xsl:attribute name="height"><xsl:value-of select="$oidSize"/></xsl:attribute>
            <xsl:attribute name="patternTransform">translate(0,0)</xsl:attribute>
            <xsl:attribute name="patternUnits">userSpaceOnUse</xsl:attribute>
            <svg:image x="0" y="0">
                <xsl:attribute name="width"><xsl:value-of select="$oidSize"/></xsl:attribute>
                <xsl:attribute name="height"><xsl:value-of select="$oidSize"/></xsl:attribute>
                <xsl:attribute name="xlink:href">./oid-<xsl:value-of select="$productId"/>-START<xsl:value-of select="$oidSuffix"/>.png</xsl:attribute>
            </svg:image>
        </svg:pattern>
    </xsl:copy>
</xsl:template>


<xsl:template match="//*[contains(string(svg:desc[1]), &quot;oid&quot;)]">
    <svg:g>
        <xsl:copy-of select="."/>
        <xsl:apply-templates select="." mode="restyle"/>
    </svg:g>
</xsl:template>

<xsl:template match="/svg:svg">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
        <xsl:if test="$needs-start-button">
            <svg:g
                inkscape:label="ttbox-start-button"
                inkscape:groupmode="layer"
                id="ttbox-start-button">
                <svg:g>
                    <xsl:attribute name="transform">translate(0,<xsl:value-of select="concat(substring(substring-before(@height,&quot;mm&quot;) * 90 * 10 div 254, 1, number(contains(@height,&quot;mm&quot;))*(string-length(@height)+10)), substring(@height, 1, number(not(contains(@height,&quot;mm&quot;)))*string-length(@height)))"/>)</xsl:attribute>
                    <svg:g transform="translate(53.1496063, -53.1496063)" >
                        <svg:circle
                            style="color:#000000;fill:#00ff00;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:0.35433072;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
                            r="17.716536"
                            cy="0"
                            cx="0" />
                        <svg:path
                            sodipodi:type="arc"
                            style="color:#000000;fill:none;stroke:#ffffff;stroke-width:4.03460884;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate"
                            sodipodi:cx="43.121025"
                            sodipodi:cy="953.5824"
                            sodipodi:rx="11.957932"
                            sodipodi:ry="12.247821"
                            d="M 55.078958,953.5824 A 11.957932,12.247821 0 1 1 49.099992,942.97547"
                            sodipodi:start="0"
                            sodipodi:end="5.2359878"
                            transform="matrix(0.43911887,-0.76056517,0.76057068,0.43910932,-744.24477,-385.92484)"
                            sodipodi:open="true" />
                        <svg:path
                            style="fill:none;stroke:#ffffff;stroke-width:3.54330707;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none"
                            d="m 1e-6,-12.17537 0,8.11686"
                            inkscape:connector-curvature="0"
                            sodipodi:nodetypes="cc" />
                        <svg:circle
                            style="fill:url(#pattern-oid-START);fill-opacity:1"
                            r="17.716536"
                            cy="0"
                            cx="0" />
                    </svg:g>
                </svg:g>
            </svg:g>
        </xsl:if>
    </xsl:copy>
</xsl:template>

<xsl:template match="node()|@*">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
    </xsl:copy>
</xsl:template>

<xsl:template match="node()|@*" mode="restyle">
    <xsl:copy>
        <xsl:apply-templates select="node()|@*" mode="restyle"/>
    </xsl:copy>
</xsl:template>


</xsl:stylesheet>
