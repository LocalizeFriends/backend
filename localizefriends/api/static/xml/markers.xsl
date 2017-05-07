<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml">

    <xsl:output method="xml" indent="yes"
        doctype-public="-//W3C//DTD XHTML 1.1//EN"
        doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"/>

    <xsl:template match="markers">
        <html>
            <head>
                <title>Miejsca</title>
                <link rel="stylesheet" href="markers.css"/>
            </head>
            <body>
                <h1>Lista miejsc</h1>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="marker">
        <h2><xsl:value-of select="@name"/></h2>
        <dl>
            <dt>szerokość geograficzna</dt>
            <dd><xsl:value-of select="@lat"/></dd>
            <dt>długość geograficzna</dt>
            <dd><xsl:value-of select="@lng"/></dd>
        </dl>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="description">
        <div><xsl:value-of select="."/></div>
    </xsl:template>
</xsl:stylesheet>
