#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 mrg <mrg@MrG-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
"""

import os

f = open( "index.html", "w" )

f.write( "<html>\n" )
f.write( "<head>\n" )
#f.write( "<title>Template {{ title }}</title>" )
f.write( "</head>\n" )
f.write( "<body>\n" )
for img in os.listdir( "./output/" ) :
  if not img[-3:] == "txt" :
    f.write( "<img src='{}'>\n".format( "./output/" + img ) )
f.write( "</body>\n" )
f.write( "</html>\n" )

f.close()

