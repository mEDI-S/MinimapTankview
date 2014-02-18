@echo off

swfmill swf2xml Minimap.swf Minimap.swf.xml
patch --binary -p0 < minimap_arrow.patch
swfmill xml2swf Minimap.swf.xml Minimap_arrow.swf

swfmill swf2xml Minimap.swf Minimap.swf.xml
patch --binary -p0 < Minimap_line.patch
swfmill xml2swf Minimap.swf.xml Minimap_line.swf
