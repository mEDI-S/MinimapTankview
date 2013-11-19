@echo off

swfmill swf2xml Minimap.swf Minimap.swf.xml
patch --binary -p0 < minimap.patch
swfmill xml2swf Minimap.swf.xml Minimap_new.swf
