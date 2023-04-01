<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="PREFIX/object/class[@name='FUNCTION']/object">
    <Item>
       <xsl:for-each select="parameter">
          <xsl:element name="{@name}"><xsl:value-of select="@value"/></xsl:element>
       </xsl:for-each>
    </Item>
</xsl:template>
</xsl:stylesheet>
