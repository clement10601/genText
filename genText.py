#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 mrg <mrg@MrG-MacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
Generate Traditional Chinese Image
"""

from PIL import Image, ImageDraw, ImageFont  
import argparse
import os
import random
import uuid
import codecs

#fontPath = 'fonts/'
fontPath = 'Fonts.new/'
outputPath = 'output/'
imageType = '.jpg'
imageHeight = 50

def genLabel( text, im_h, im_w, outputName ) :
  f = codecs.open( outputName, encoding='utf-8', mode="w+" )
  f.write( u"{}\n{}\n{}".format(  text, im_h, im_w ) )
  f.close()

def genImageAndLabel( text ) :
  """
  generate image one line
  """
  #text = u'中文測試繁體中文'
  #text = u'不要嘴砲了'
  #text = u'test English'

  # for English character
  isEnglish = False
  if ord( text[0] ) <= ord( u'z' ) :
    isEnglish = True
  
  im_height = imageHeight
  im_width = len( text ) * im_height / ( 2 if isEnglish else 1 )

  outputName = str( uuid.uuid4() )
  
  ## for generating colorful background and foreground
  #for f_r in xrange( 256 ) :
  #  for f_g in xrange( 256 ) :
  #    for f_b in xrange( 256 ) :
  #      for b_r in xrange( 256 ) :
  #        for b_g in xrange( 256 ) :
  #          for b_b in xrange( 256 ) :

  f_r = 0
  f_g = 0
  f_b = 0
  b_r = 255
  b_g = 255
  b_b = 255

  count = 0
  for dirPath, dirNames, fileNames in os.walk( fontPath ):
    for index, f in enumerate( fileNames ) :

      # ignore ".DS_store"
      if f[0] == '.' :
        continue

      #print os.path.split( dirPath )[-1]
      font = os.path.join(dirPath, f)
      #print font
      im = Image.new( 'RGB', ( im_width, im_height ), color=( b_r, b_g, b_b ) )
      
      draw = ImageDraw.Draw(im)
      draw.text( ( 0, 0 ), 
                 text, 
                 font=ImageFont.truetype( font, size=imageHeight ), 
                 fill=( f_r, f_g, f_b ) )
      
      #im.show()
      im.save( outputPath + outputName +
               str( count ) +
               str( index ) +
               #os.path.split( dirPath )[-1] + 
               #f + 
               imageType )
    count += 1

  genLabel( text, im_height, im_width, outputPath + outputName + ".txt" )

def batchGenImage( fileName ) :
  """
  read txt line by line to generate image
  """
  with open( fileName ) as f:
    for line in f.readlines() :
      text = line.strip() # remove white space
      text = unicode( text, "utf-8" ) # convert to utf-8
      text = text.replace( u'　', '' ) # remove fullwidth forms space
      text = text.replace( u'\n', '' ) # remove 0x0A
      print len( text )
      print text
      genImageAndLabel( text )

def characterGenImage( fileName ) :
  """
  every character generate a image
  """
  with open( fileName ) as f:
    # remove white space and convert to utf-8
    context = unicode( f.read().strip(), "utf-8" ) 
    context = context.replace( u'\n', '' ) # remove 0x0A
    for text in context :
      genImageAndLabel( text )

def sentenceGenImage( fileName, maxNumber ) :
  """
  """
  with open( fileName ) as f:
    # remove white space and convert to utf-8
    context = unicode( f.read().strip(), "utf-8" )
    context = context.replace( u'　', '' ) # remove fullwidth forms space
    context = context.replace( u'\n', '' ) # remove 0x0A
    index = 0
    contextSize = len( context )

    while ( index < contextSize ) :
      textSize = random.randrange( 1, 1 + maxNumber )
      print textSize
      print( context[index : index + textSize] )
      print "--------------"
      genImageAndLabel( context[index : index + textSize] )
      index += textSize

if __name__ == '__main__' :
  parser = argparse.ArgumentParser()
  parser.add_argument( "-f", "--file", help='use txt file' )
  parser.add_argument( "-l", "--line", action='store_true', 
                       help='use txt file and line/image' )
  parser.add_argument( "-c", "--character", action='store_true',
                       help='use txt file and character/image' )
  parser.add_argument( "-s", "--sentence", metavar='N_character(s)', type=int,
                       help='use txt file and N character(s) per image' )
  parser.add_argument( "-t", "--text",  type=lambda s: unicode(s, 'utf8'),
                       help='input text to generate text' )
  parser.add_argument( "-d", "--debug", action='store_true',
                       help='use debug mode' )
  args = parser.parse_args()

  if not os.path.isdir( outputPath ) :
    os.mkdir( outputPath )
  
  if args.file and args.line :
    batchGenImage( args.file ) 
  elif args.file and args.character :
    characterGenImage( args.file )
  elif args.file and args.sentence :
    sentenceGenImage( args.file, args.sentence )
  elif args.text :
    genImageAndLabel( args.text )
  elif args.file : # missing arguments
    parser.error( "--file require --line or --character or --sentence" )
  else : # no argument
    parser.print_help()


