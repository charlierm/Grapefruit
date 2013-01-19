#!/usr/bin/python
# -*- coding: utf-8 -*-#

# Copyright (c) 2008, Xavier Basty
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''GrapeFruit - Colour manipulation in Python'''

from __future__ import division

import sys

# $Id$
__author__ = 'Xavier Basty <xbasty@gmail.com>'
__version__ = '0.1a3'


# The default white reference, use 2° Standard Observer, D65 (daylight)
_DEFAULT_WREF = (0.95043, 1.00000, 1.08890)

_oneThird = 1.0 / 3
_srgbGammaCorrInv = 0.03928 / 12.92
_sixteenHundredsixteenth = 16.0 / 116

_RybWheel = (
    0,  26,  52,
   83, 120, 130,
  141, 151, 162,
  177, 190, 204,
  218, 232, 246,
  261, 275, 288,
  303, 317, 330,
  338, 345, 352,
  360)

_RgbWheel = (
    0,   8,  17,
   26,  34,  41,
   48,  54,  60,
   81, 103, 123,
  138, 155, 171,
  187, 204, 219,
  234, 251, 267,
  282, 298, 329,
  360)

class Colour:
  '''Hold a Colour value.

  Example usage:

  To create an instance of the grapefruit.Colour from RGB values:

    >>> import grapefruit
    >>> r, g, b = 1, 0.5, 0
    >>> col = grapefruit.Colour.NewFromRgb(r, g, b)

  To get the values of the Colour in another Colourspace:

    >>> h, s, v = col.hsv
    >>> l, a, b = col.lab

  To get the complementary of a Colour:

    >>> compl = col.ComplementaryColour(mode='rgb')
    >>> print(compl.hsl)
    (210.0, 1.0, 0.5)

  To directly convert RGB values to their HSL equivalent:

    >>> h, s, l = Colour.RgbToHsl(r, g, b)

  '''

  WHITE_REFERENCE = {
    'std_A'       : (1.09847, 1.00000, 0.35582),
    'std_B'       : (0.99093, 1.00000, 0.85313),
    'std_C'       : (0.98071, 1.00000, 1.18225),
    'std_D50'     : (0.96421, 1.00000, 0.82519),
    'std_D55'     : (0.95680, 1.00000, 0.92148),
    'std_D65'     : (0.95043, 1.00000, 1.08890),
    'std_D75'     : (0.94972, 1.00000, 1.22639),
    'std_E'       : (1.00000, 1.00000, 1.00000),
    'std_F1'      : (0.92834, 1.00000, 1.03665),
    'std_F2'      : (0.99145, 1.00000, 0.67316),
    'std_F3'      : (1.03753, 1.00000, 0.49861),
    'std_F4'      : (1.09147, 1.00000, 0.38813),
    'std_F5'      : (0.90872, 1.00000, 0.98723),
    'std_F6'      : (0.97309, 1.00000, 0.60191),
    'std_F7'      : (0.95017, 1.00000, 1.08630),
    'std_F8'      : (0.96413, 1.00000, 0.82333),
    'std_F9'      : (1.00365, 1.00000, 0.67868),
    'std_F10'     : (0.96174, 1.00000, 0.81712),
    'std_F11'     : (1.00899, 1.00000, 0.64262),
    'std_F12'     : (1.08046, 1.00000, 0.39228),
    'sup_A'       : (1.11142, 1.00000, 0.35200),
    'sup_B'       : (0.99178, 1.00000, 0.84349),
    'sup_C'       : (0.97286, 1.00000, 1.16145),
    'sup_D50'     : (0.96721, 1.00000, 0.81428),
    'sup_D55'     : (0.95797, 1.00000, 0.90925),
    'sup_D65'     : (0.94810, 1.00000, 1.07305),
    'sup_D75'     : (0.94417, 1.00000, 1.20643),
    'sup_E'       : (1.00000, 1.00000, 1.00000),
    'sup_F1'      : (0.94791, 1.00000, 1.03191),
    'sup_F2'      : (1.03245, 1.00000, 0.68990),
    'sup_F3'      : (1.08968, 1.00000, 0.51965),
    'sup_F4'      : (1.14961, 1.00000, 0.40963),
    'sup_F5'      : (0.93369, 1.00000, 0.98636),
    'sup_F6'      : (1.02148, 1.00000, 0.62074),
    'sup_F7'      : (0.95780, 1.00000, 1.07618),
    'sup_F8'      : (0.97115, 1.00000, 0.81135),
    'sup_F9'      : (1.02116, 1.00000, 0.67826),
    'sup_F10'     : (0.99001, 1.00000, 0.83134),
    'sup_F11'     : (1.03820, 1.00000, 0.65555),
    'sup_F12'     : (1.11428, 1.00000, 0.40353)}

  NAMED_Colour = {
    'aliceblue':            '#f0f8ff',
    'antiquewhite':         '#faebd7',
    'aqua':                 '#00ffff',
    'aquamarine':           '#7fffd4',
    'azure':                '#f0ffff',
    'beige':                '#f5f5dc',
    'bisque':               '#ffe4c4',
    'black':                '#000000',
    'blanchedalmond':       '#ffebcd',
    'blue':                 '#0000ff',
    'blueviolet':           '#8a2be2',
    'brown':                '#a52a2a',
    'burlywood':            '#deb887',
    'cadetblue':            '#5f9ea0',
    'chartreuse':           '#7fff00',
    'chocolate':            '#d2691e',
    'coral':                '#ff7f50',
    'cornflowerblue':       '#6495ed',
    'cornsilk':             '#fff8dc',
    'crimson':              '#dc143c',
    'cyan':                 '#00ffff',
    'darkblue':             '#00008b',
    'darkcyan':             '#008b8b',
    'darkgoldenrod':        '#b8860b',
    'darkgray':             '#a9a9a9',
    'darkgrey':             '#a9a9a9',
    'darkgreen':            '#006400',
    'darkkhaki':            '#bdb76b',
    'darkmagenta':          '#8b008b',
    'darkolivegreen':       '#556b2f',
    'darkorange':           '#ff8c00',
    'darkorchid':           '#9932cc',
    'darkred':              '#8b0000',
    'darksalmon':           '#e9967a',
    'darkseagreen':         '#8fbc8f',
    'darkslateblue':        '#483d8b',
    'darkslategray':        '#2f4f4f',
    'darkslategrey':        '#2f4f4f',
    'darkturquoise':        '#00ced1',
    'darkviolet':           '#9400d3',
    'deeppink':             '#ff1493',
    'deepskyblue':          '#00bfff',
    'dimgray':              '#696969',
    'dimgrey':              '#696969',
    'dodgerblue':           '#1e90ff',
    'firebrick':            '#b22222',
    'floralwhite':          '#fffaf0',
    'forestgreen':          '#228b22',
    'fuchsia':              '#ff00ff',
    'gainsboro':            '#dcdcdc',
    'ghostwhite':           '#f8f8ff',
    'gold':                 '#ffd700',
    'goldenrod':            '#daa520',
    'gray':                 '#808080',
    'grey':                 '#808080',
    'green':                '#008000',
    'greenyellow':          '#adff2f',
    'honeydew':             '#f0fff0',
    'hotpink':              '#ff69b4',
    'indianred':            '#cd5c5c',
    'indigo':               '#4b0082',
    'ivory':                '#fffff0',
    'khaki':                '#f0e68c',
    'lavender':             '#e6e6fa',
    'lavenderblush':        '#fff0f5',
    'lawngreen':            '#7cfc00',
    'lemonchiffon':         '#fffacd',
    'lightblue':            '#add8e6',
    'lightcoral':           '#f08080',
    'lightcyan':            '#e0ffff',
    'lightgoldenrodyellow': '#fafad2',
    'lightgreen':           '#90ee90',
    'lightgray':            '#d3d3d3',
    'lightgrey':            '#d3d3d3',
    'lightpink':            '#ffb6c1',
    'lightsalmon':          '#ffa07a',
    'lightseagreen':        '#20b2aa',
    'lightskyblue':         '#87cefa',
    'lightslategray':       '#778899',
    'lightslategrey':       '#778899',
    'lightsteelblue':       '#b0c4de',
    'lightyellow':          '#ffffe0',
    'lime':                 '#00ff00',
    'limegreen':            '#32cd32',
    'linen':                '#faf0e6',
    'magenta':              '#ff00ff',
    'maroon':               '#800000',
    'mediumaquamarine':     '#66cdaa',
    'mediumblue':           '#0000cd',
    'mediumorchid':         '#ba55d3',
    'mediumpurple':         '#9370db',
    'mediumseagreen':       '#3cb371',
    'mediumslateblue':      '#7b68ee',
    'mediumspringgreen':    '#00fa9a',
    'mediumturquoise':      '#48d1cc',
    'mediumvioletred':      '#c71585',
    'midnightblue':         '#191970',
    'mintcream':            '#f5fffa',
    'mistyrose':            '#ffe4e1',
    'moccasin':             '#ffe4b5',
    'navajowhite':          '#ffdead',
    'navy':                 '#000080',
    'oldlace':              '#fdf5e6',
    'olive':                '#808000',
    'olivedrab':            '#6b8e23',
    'orange':               '#ffa500',
    'orangered':            '#ff4500',
    'orchid':               '#da70d6',
    'palegoldenrod':        '#eee8aa',
    'palegreen':            '#98fb98',
    'paleturquoise':        '#afeeee',
    'palevioletred':        '#db7093',
    'papayawhip':           '#ffefd5',
    'peachpuff':            '#ffdab9',
    'peru':                 '#cd853f',
    'pink':                 '#ffc0cb',
    'plum':                 '#dda0dd',
    'powderblue':           '#b0e0e6',
    'purple':               '#800080',
    'red':                  '#ff0000',
    'rosybrown':            '#bc8f8f',
    'royalblue':            '#4169e1',
    'saddlebrown':          '#8b4513',
    'salmon':               '#fa8072',
    'sandybrown':           '#f4a460',
    'seagreen':             '#2e8b57',
    'seashell':             '#fff5ee',
    'sienna':               '#a0522d',
    'silver':               '#c0c0c0',
    'skyblue':              '#87ceeb',
    'slateblue':            '#6a5acd',
    'slategray':            '#708090',
    'slategrey':            '#708090',
    'snow':                 '#fffafa',
    'springgreen':          '#00ff7f',
    'steelblue':            '#4682b4',
    'tan':                  '#d2b48c',
    'teal':                 '#008080',
    'thistle':              '#d8bfd8',
    'tomato':               '#ff6347',
    'turquoise':            '#40e0d0',
    'violet':               '#ee82ee',
    'wheat':                '#f5deb3',
    'white':                '#ffffff',
    'whitesmoke':           '#f5f5f5',
    'yellow':               '#ffff00',
    'yellowgreen':          '#9acd32'}

  def __init__(self, values, mode='rgb', alpha=1.0, wref=_DEFAULT_WREF):
    '''Instantiate a new grapefruit.Colour object.

    Parameters:
      :values:
        The values of this Colour, in the specified representation.
      :mode:
        The representation mode used for values.
      :alpha:
        the alpha value (transparency) of this Colour.
      :wref:
        The whitepoint reference, default is 2° D65.

    '''
    if not(isinstance(values, tuple)):
      raise TypeError('values must be a tuple')

    if mode=='rgb':
      self.__rgb = values
      self.__hsl = Colour.RgbToHsl(*values)
    elif mode=='hsl':
      self.__hsl = values
      self.__rgb = Colour.HslToRgb(*values)
    else:
      raise ValueError('Invalid Colour mode: ' + mode)

    self.__a = alpha
    self.__wref = wref

  def __ne__(self, other):
    return not self.__eq__(other)

  def __eq__(self, other):
    try:
      if isinstance(other, Colour):
        return (self.__rgb==other.__rgb) and (self.__a==other.__a)
      if len(other) != 4:
        return False
      return list(self.__rgb + (self.__a,)) == list(other)
    except TypeError:
      return False
    except AttributeError:
      return False

  def __repr__(self):
    return str(self.__rgb + (self.__a,))

  def __str__(self):
    '''A string representation of this grapefruit.Colour instance.

    Returns:
      The RGBA representation of this grapefruit.Colour instance.

    '''
    return '(%g, %g, %g, %g)' % (self.__rgb + (self.__a,))

  if sys.version_info[0] < 3:
    def __unicode__(self):
      '''A unicode string representation of this grapefruit.Colour instance.

      Returns:
        The RGBA representation of this grapefruit.Colour instance.

      '''
      return unicode('%g, %g, %g, %g)') % (self.__rgb + (self.__a,))

  def __iter__(self):
    return iter(self.__rgb + (self.__a,))

  def __len__(self):
    return 4

  def __GetIsLegal(self):
    return all(0.0 <= v <= 1.0 for v in self)
  isLegal = property(fget=__GetIsLegal, doc='Boolean indicating whether the Colour is within the legal gamut.')

  def __GetNearestLegal(self):
    def clamp(x, lo, hi):
      if x < lo:
        return lo
      elif x > hi:
        return hi
      else:
        return x
    return Colour.NewFromRgb(*[clamp(v, 0.0, 1.0) for v in self])
  nearestLegal = property(fget=__GetNearestLegal, doc='The nearest legal Colour.')

  @staticmethod
  def RgbToHsl(r, g, b):
    '''Convert the Colour from RGB coordinates to HSL.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (h, s, l) tuple in the range:
      h[0...360],
      s[0...1],
      l[0...1]

    >>> Colour.RgbToHsl(1, 0.5, 0)
    (30.0, 1.0, 0.5)

    '''
    minVal = min(r, g, b)       # min RGB value
    maxVal = max(r, g, b)       # max RGB value

    l = (maxVal + minVal) / 2.0
    if minVal==maxVal:
      return (0.0, 0.0, l)    # achromatic (gray)

    d = maxVal - minVal         # delta RGB value

    if l < 0.5: s = d / (maxVal + minVal)
    else: s = d / (2.0 - maxVal - minVal)

    dr, dg, db = [(maxVal-val) / d for val in (r, g, b)]

    if r==maxVal:
      h = db - dg
    elif g==maxVal:
      h = 2.0 + dr - db
    else:
      h = 4.0 + dg - dr

    h = (h*60.0) % 360.0
    return (h, s, l)

  @staticmethod
  def _HueToRgb(n1, n2, h):
    h %= 6.0
    if h < 1.0: return n1 + ((n2-n1) * h)
    if h < 3.0: return n2
    if h < 4.0: return n1 + ((n2-n1) * (4.0 - h))
    return n1

  @staticmethod
  def HslToRgb(h, s, l):
    '''Convert the Colour from HSL coordinates to RGB.

    Parameters:
      :h:
        The Hue component value [0...1]
      :s:
        The Saturation component value [0...1]
      :l:
        The Lightness component value [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> Colour.HslToRgb(30.0, 1.0, 0.5)
    (1.0, 0.5, 0.0)

    '''
    if s==0: return (l, l, l)   # achromatic (gray)

    if l<0.5: n2 = l * (1.0 + s)
    else: n2 = l+s - (l*s)

    n1 = (2.0 * l) - n2

    h /= 60.0
    hueToRgb = Colour._HueToRgb
    r = hueToRgb(n1, n2, h + 2)
    g = hueToRgb(n1, n2, h)
    b = hueToRgb(n1, n2, h - 2)

    return (r, g, b)

  @staticmethod
  def RgbToHsv(r, g, b):
    '''Convert the Colour from RGB coordinates to HSV.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (h, s, v) tuple in the range:
      h[0...360],
      s[0...1],
      v[0...1]

    >>> Colour.RgbToHsv(1, 0.5, 0)
    (30.0, 1.0, 1.0)

    '''
    v = float(max(r, g, b))
    d = v - min(r, g, b)
    if d==0: return (0.0, 0.0, v)
    s = d / v

    dr, dg, db = [(v - val) / d for val in (r, g, b)]

    if r==v:
      h = db - dg             # between yellow & magenta
    elif g==v:
      h = 2.0 + dr - db       # between cyan & yellow
    else: # b==v
      h = 4.0 + dg - dr       # between magenta & cyan

    h = (h*60.0) % 360.0
    return (h, s, v)

  @staticmethod
  def HsvToRgb(h, s, v):
    '''Convert the Colour from RGB coordinates to HSV.

    Parameters:
      :h:
        The Hus component value [0...1]
      :s:
        The Saturation component value [0...1]
      :v:
        The Value component [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> Colour.HslToRgb(30.0, 1.0, 0.5)
    (1.0, 0.5, 0.0)

    '''
    if s==0: return (v, v, v)   # achromatic (gray)

    h /= 60.0
    h = h % 6.0

    i = int(h)
    f = h - i
    if not(i&1): f = 1-f     # if i is even

    m = v * (1.0 - s)
    n = v * (1.0 - (s * f))

    if i==0: return (v, n, m)
    if i==1: return (n, v, m)
    if i==2: return (m, v, n)
    if i==3: return (m, n, v)
    if i==4: return (n, m, v)
    return (v, m, n)

  @staticmethod
  def RgbToYiq(r, g, b):
    '''Convert the Colour from RGB to YIQ.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (y, i, q) tuple in the range:
      y[0...1],
      i[0...1],
      q[0...1]

    >>> '(%g, %g, %g)' % Colour.RgbToYiq(1, 0.5, 0)
    '(0.592263, 0.458874, -0.0499818)'

    '''
    y = (r * 0.29895808) + (g * 0.58660979) + (b *0.11443213)
    i = (r * 0.59590296) - (g * 0.27405705) - (b *0.32184591)
    q = (r * 0.21133576) - (g * 0.52263517) + (b *0.31129940)
    return (y, i, q)

  @staticmethod
  def YiqToRgb(y, i, q):
    '''Convert the Colour from YIQ coordinates to RGB.

    Parameters:
      :y:
        Tte Y component value [0...1]
      :i:
        The I component value [0...1]
      :q:
        The Q component value [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> '(%g, %g, %g)' % Colour.YiqToRgb(0.592263, 0.458874, -0.0499818)
    '(1, 0.5, 5.442e-07)'

    '''
    r = y + (i * 0.9562) + (q * 0.6210)
    g = y - (i * 0.2717) - (q * 0.6485)
    b = y - (i * 1.1053) + (q * 1.7020)
    return (r, g, b)

  @staticmethod
  def RgbToYuv(r, g, b):
    '''Convert the Colour from RGB coordinates to YUV.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (y, u, v) tuple in the range:
      y[0...1],
      u[-0.436...0.436],
      v[-0.615...0.615]

    >>> '(%g, %g, %g)' % Colour.RgbToYuv(1, 0.5, 0)
    '(0.5925, -0.29156, 0.357505)'

    '''
    y =  (r * 0.29900) + (g * 0.58700) + (b * 0.11400)
    u = -(r * 0.14713) - (g * 0.28886) + (b * 0.43600)
    v =  (r * 0.61500) - (g * 0.51499) - (b * 0.10001)
    return (y, u, v)

  @staticmethod
  def YuvToRgb(y, u, v):
    '''Convert the Colour from YUV coordinates to RGB.

    Parameters:
      :y:
        The Y component value [0...1]
      :u:
        The U component value [-0.436...0.436]
      :v:
        The V component value [-0.615...0.615]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> '(%g, %g, %g)' % Colour.YuvToRgb(0.5925, -0.2916, 0.3575)
    '(0.999989, 0.500015, -6.3276e-05)'

    '''
    r = y + (v * 1.13983)
    g = y - (u * 0.39465) - (v * 0.58060)
    b = y + (u * 2.03211)
    return (r, g, b)

  @staticmethod
  def RgbToXyz(r, g, b):
    '''Convert the Colour from sRGB to CIE XYZ.

    The methods assumes that the RGB coordinates are given in the sRGB
    Colourspace (D65).

    .. note::

       Compensation for the sRGB gamma correction is applied before converting.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (x, y, z) tuple in the range:
      x[0...1],
      y[0...1],
      z[0...1]

    >>> '(%g, %g, %g)' % Colour.RgbToXyz(1, 0.5, 0)
    '(0.488941, 0.365682, 0.0448137)'

    '''
    r, g, b = [((v <= 0.03928) and [v / 12.92] or [((v+0.055) / 1.055) **2.4])[0] for v in (r, g, b)]

    x = (r * 0.4124) + (g * 0.3576) + (b * 0.1805)
    y = (r * 0.2126) + (g * 0.7152) + (b * 0.0722)
    z = (r * 0.0193) + (g * 0.1192) + (b * 0.9505)
    return (x, y, z)

  @staticmethod
  def XyzToRgb(x, y, z):
    '''Convert the Colour from CIE XYZ coordinates to sRGB.

    .. note::

       Compensation for sRGB gamma correction is applied before converting.

    Parameters:
      :x:
        The X component value [0...1]
      :y:
        The Y component value [0...1]
      :z:
        The Z component value [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> '(%g, %g, %g)' % Colour.XyzToRgb(0.488941, 0.365682, 0.0448137)
    '(1, 0.5, 6.81883e-08)'

    '''
    r =  (x * 3.2406255) - (y * 1.5372080) - (z * 0.4986286)
    g = -(x * 0.9689307) + (y * 1.8757561) + (z * 0.0415175)
    b =  (x * 0.0557101) - (y * 0.2040211) + (z * 1.0569959)
    return tuple((((v <= _srgbGammaCorrInv) and [v * 12.92] or [(1.055 * (v ** (1/2.4))) - 0.055])[0] for v in (r, g, b)))

  @staticmethod
  def XyzToLab(x, y, z, wref=_DEFAULT_WREF):
    '''Convert the Colour from CIE XYZ to CIE L*a*b*.

    Parameters:
      :x:
        The X component value [0...1]
      :y:
        The Y component value [0...1]
      :z:
        The Z component value [0...1]
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      The Colour as an (L, a, b) tuple in the range:
      L[0...100],
      a[-1...1],
      b[-1...1]

    >>> '(%g, %g, %g)' % Colour.XyzToLab(0.488941, 0.365682, 0.0448137)
    '(66.9518, 0.43084, 0.739692)'

    >>> '(%g, %g, %g)' % Colour.XyzToLab(0.488941, 0.365682, 0.0448137, Colour.WHITE_REFERENCE['std_D50'])
    '(66.9518, 0.411663, 0.67282)'

    '''
    # White point correction
    x /= wref[0]
    y /= wref[1]
    z /= wref[2]

    # Nonlinear distortion and linear transformation
    x, y, z = [((v > 0.008856) and [v**_oneThird] or [(7.787 * v) + _sixteenHundredsixteenth])[0] for v in (x, y, z)]

    # Vector scaling
    l = (116 * y) - 16
    a = 5.0 * (x - y)
    b = 2.0 * (y - z)

    return (l, a, b)

  @staticmethod
  def LabToXyz(l, a, b, wref=_DEFAULT_WREF):
    '''Convert the Colour from CIE L*a*b* to CIE 1931 XYZ.

    Parameters:
      :l:
        The L component [0...100]
      :a:
        The a component [-1...1]
      :b:
        The a component [-1...1]
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      The Colour as an (x, y, z) tuple in the range:
      x[0...q],
      y[0...1],
      z[0...1]

    >>> '(%g, %g, %g)' % Colour.LabToXyz(66.9518, 0.43084, 0.739692)
    '(0.488941, 0.365682, 0.0448137)'

    >>> '(%g, %g, %g)' % Colour.LabToXyz(66.9518, 0.411663, 0.67282, Colour.WHITE_REFERENCE['std_D50'])
    '(0.488941, 0.365682, 0.0448138)'

    '''
    y = (l + 16) / 116
    x = (a / 5.0) + y
    z = y - (b / 2.0)
    return tuple((((v > 0.206893) and [v**3] or [(v - _sixteenHundredsixteenth) / 7.787])[0] * w for v, w in zip((x, y, z), wref)))

  @staticmethod
  def CmykToCmy(c, m, y, k):
    '''Convert the Colour from CMYK coordinates to CMY.

    Parameters:
      :c:
        The Cyan component value [0...1]
      :m:
        The Magenta component value [0...1]
      :y:
        The Yellow component value [0...1]
      :k:
        The Black component value [0...1]

    Returns:
      The Colour as an (c, m, y) tuple in the range:
      c[0...1],
      m[0...1],
      y[0...1]

    >>> '(%g, %g, %g)' % Colour.CmykToCmy(1, 0.32, 0, 0.5)
    '(1, 0.66, 0.5)'

    '''
    mk = 1-k
    return ((c*mk + k), (m*mk + k), (y*mk + k))

  @staticmethod
  def CmyToCmyk(c, m, y):
    '''Convert the Colour from CMY coordinates to CMYK.

    Parameters:
      :c:
        The Cyan component value [0...1]
      :m:
        The Magenta component value [0...1]
      :y:
        The Yellow component value [0...1]

    Returns:
      The Colour as an (c, m, y, k) tuple in the range:
      c[0...1],
      m[0...1],
      y[0...1],
      k[0...1]

    >>> '(%g, %g, %g, %g)' % Colour.CmyToCmyk(1, 0.66, 0.5)
    '(1, 0.32, 0, 0.5)'

    '''
    k = min(c, m, y)
    if k==1.0: return (0.0, 0.0, 0.0, 1.0)
    mk = 1-k
    return ((c-k) / mk, (m-k) / mk, (y-k) / mk, k)

  @staticmethod
  def RgbToCmy(r, g, b):
    '''Convert the Colour from RGB coordinates to CMY.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (c, m, y) tuple in the range:
      c[0...1],
      m[0...1],
      y[0...1]

    >>> Colour.RgbToCmy(1, 0.5, 0)
    (0, 0.5, 1)

    '''
    return (1-r, 1-g, 1-b)

  @staticmethod
  def CmyToRgb(c, m, y):
    '''Convert the Colour from CMY coordinates to RGB.

    Parameters:
      :c:
        The Cyan component value [0...1]
      :m:
        The Magenta component value [0...1]
      :y:
        The Yellow component value [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> Colour.CmyToRgb(0, 0.5, 1)
    (1, 0.5, 0)

    '''
    return (1-c, 1-m, 1-y)

  @staticmethod
  def RgbToIntTuple(r, g, b):
    '''Convert the Colour from (r, g, b) to an int tuple.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...255],
      g[0...2551],
      b[0...2551]

    >>> Colour.RgbToIntTuple(1, 0.5, 0)
    (255, 128, 0)

    '''
    return tuple(int(round(v*255)) for v in (r, g, b))

  @staticmethod
  def IntTupleToRgb(intTuple):
    '''Convert a tuple of ints to (r, g, b).

    Parameters:
      The Colour as an (r, g, b) integer tuple in the range:
      r[0...255],
      g[0...255],
      b[0...255]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> '(%g, %g, %g)' % Colour.IntTupleToRgb((255, 128, 0))
    '(1, 0.501961, 0)'

    '''
    return tuple(v / 255 for v in intTuple)

  @staticmethod
  def RgbToHtml(r, g, b):
    '''Convert the Colour from (r, g, b) to #RRGGBB.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      A CSS string representation of this Colour (#RRGGBB).

    >>> Colour.RgbToHtml(1, 0.5, 0)
    '#ff8000'

    '''
    return '#%02x%02x%02x' % tuple((min(round(v*255), 255) for v in (r, g, b)))

  @staticmethod
  def HtmlToRgb(html):
    '''Convert the HTML Colour to (r, g, b).

    Parameters:
      :html:
        the HTML definition of the Colour (#RRGGBB or #RGB or a Colour name).

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      r[0...1],
      g[0...1],
      b[0...1]

    Throws:
      :ValueError:
        If html is neither a known Colour name or a hexadecimal RGB
        representation.

    >>> '(%g, %g, %g)' % Colour.HtmlToRgb('#ff8000')
    '(1, 0.501961, 0)'
    >>> '(%g, %g, %g)' % Colour.HtmlToRgb('ff8000')
    '(1, 0.501961, 0)'
    >>> '(%g, %g, %g)' % Colour.HtmlToRgb('#f60')
    '(1, 0.4, 0)'
    >>> '(%g, %g, %g)' % Colour.HtmlToRgb('f60')
    '(1, 0.4, 0)'
    >>> '(%g, %g, %g)' % Colour.HtmlToRgb('lemonchiffon')
    '(1, 0.980392, 0.803922)'

    '''
    html = html.strip().lower()
    if html[0]=='#':
      html = html[1:]
    elif html in Colour.NAMED_Colour:
      html = Colour.NAMED_Colour[html][1:]

    if len(html)==6:
      rgb = html[:2], html[2:4], html[4:]
    elif len(html)==3:
      rgb = ['%c%c' % (v,v) for v in html]
    else:
      raise ValueError('input #%s is not in #RRGGBB format' % html)

    return tuple(((int(n, 16) / 255.0) for n in rgb))

  @staticmethod
  def RgbToPil(r, g, b):
    '''Convert the Colour from RGB to a PIL-compatible integer.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      A PIL compatible integer (0xBBGGRR).

    >>> '0x%06x' % Colour.RgbToPil(1, 0.5, 0)
    '0x0080ff'

    '''
    r, g, b = [min(int(round(v*255)), 255) for v in (r, g, b)]
    return (b << 16) + (g << 8) + r

  @staticmethod
  def PilToRgb(pil):
    '''Convert the Colour from a PIL-compatible integer to RGB.

    Parameters:
      pil: a PIL compatible Colour representation (0xBBGGRR)
    Returns:
      The Colour as an (r, g, b) tuple in the range:
      the range:
      r: [0...1]
      g: [0...1]
      b: [0...1]

    >>> '(%g, %g, %g)' % Colour.PilToRgb(0x0080ff)
    '(1, 0.501961, 0)'

    '''
    r = 0xff & pil
    g = 0xff & (pil >> 8)
    b = 0xff & (pil >> 16)
    return tuple((v / 255.0 for v in (r, g, b)))

  @staticmethod
  def _WebSafeComponent(c, alt=False):
    '''Convert a Colour component to its web safe equivalent.

    Parameters:
      :c:
        The component value [0...1]
      :alt:
        If True, return the alternative value instead of the nearest one.

    Returns:
      The web safe equivalent of the component value.

    '''
    # This sucks, but floating point between 0 and 1 is quite fuzzy...
    # So we just change the scale a while to make the equality tests
    # work, otherwise it gets wrong at some decimal far to the right.
    sc = c * 100.0

    # If the Colour is already safe, return it straight away
    d = sc % 20
    if d==0: return c

    # Get the lower and upper safe values
    l = sc - d
    u = l + 20

    # Return the 'closest' value according to the alt flag
    if alt:
      if (sc-l) >= (u-sc): return l/100.0
      else: return u/100.0
    else:
      if (sc-l) >= (u-sc): return u/100.0
      else: return l/100.0

  @staticmethod
  def RgbToWebSafe(r, g, b, alt=False):
    '''Convert the Colour from RGB to 'web safe' RGB

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]
      :alt:
        If True, use the alternative Colour instead of the nearest one.
        Can be used for dithering.

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> '(%g, %g, %g)' % Colour.RgbToWebSafe(1, 0.55, 0.0)
    '(1, 0.6, 0)'

    '''
    webSafeComponent = Colour._WebSafeComponent
    return tuple((webSafeComponent(v, alt) for v in (r, g, b)))

  @staticmethod
  def RgbToGreyscale(r, g, b):
    '''Convert the Colour from RGB to its greyscale equivalent

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]

    Returns:
      The Colour as an (r, g, b) tuple in the range:
      the range:
      r[0...1],
      g[0...1],
      b[0...1]

    >>> '(%g, %g, %g)' % Colour.RgbToGreyscale(1, 0.8, 0)
    '(0.6, 0.6, 0.6)'

    '''
    v = (r + g + b) / 3.0
    return (v, v, v)

  @staticmethod
  def RgbToRyb(hue):
    '''Maps a hue on the RGB Colour wheel to Itten's RYB wheel.

    Parameters:
      :hue:
        The hue on the RGB Colour wheel [0...360]

    Returns:
      An approximation of the corresponding hue on Itten's RYB wheel.

    >>> Colour.RgbToRyb(15)
    26.0

    '''
    d = hue % 15
    i = int(hue / 15)
    x0 = _RybWheel[i]
    x1 = _RybWheel[i+1]
    return x0 + (x1-x0) * d / 15

  @staticmethod
  def RybToRgb(hue):
    '''Maps a hue on Itten's RYB Colour wheel to the standard RGB wheel.

    Parameters:
      :hue:
        The hue on Itten's RYB Colour wheel [0...360]

    Returns:
      An approximation of the corresponding hue on the standard RGB wheel.

    >>> Colour.RybToRgb(15)
    8.0

    '''
    d = hue % 15
    i = int(hue / 15)
    x0 = _RgbWheel[i]
    x1 = _RgbWheel[i+1]
    return x0 + (x1-x0) * d / 15

  @staticmethod
  def NewFromRgb(r, g, b, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed RGB values.

    Parameters:
      :r:
        The Red component value [0...1]
      :g:
        The Green component value [0...1]
      :b:
        The Blue component value [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromRgb(1.0, 0.5, 0.0)
    (1.0, 0.5, 0.0, 1.0)
    >>> Colour.NewFromRgb(1.0, 0.5, 0.0, 0.5)
    (1.0, 0.5, 0.0, 0.5)

    '''
    return Colour((r, g, b), 'rgb', alpha, wref)

  @staticmethod
  def NewFromHsl(h, s, l, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed HSL values.

    Parameters:
      :h:
        The Hue component value [0...1]
      :s:
        The Saturation component value [0...1]
      :l:
        The Lightness component value [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5)
    (1.0, 0.5, 0.0, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5, 0.5)
    (1.0, 0.5, 0.0, 0.5)

    '''
    return Colour((h, s, l), 'hsl', alpha, wref)

  @staticmethod
  def NewFromHsv(h, s, v, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed HSV values.

    Parameters:
      :h:
        The Hus component value [0...1]
      :s:
        The Saturation component value [0...1]
      :v:
        The Value component [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsv(30, 1, 1)
    (1.0, 0.5, 0.0, 1.0)
    >>> Colour.NewFromHsv(30, 1, 1, 0.5)
    (1.0, 0.5, 0.0, 0.5)

    '''
    h2, s, l = Colour.RgbToHsl(*Colour.HsvToRgb(h, s, v))
    return Colour((h, s, l), 'hsl', alpha, wref)

  @staticmethod
  def NewFromYiq(y, i, q, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed YIQ values.

    Parameters:
      :y:
        The Y component value [0...1]
      :i:
        The I component value [0...1]
      :q:
        The Q component value [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromYiq(0.5922, 0.45885,-0.05))
    '(0.999902, 0.499955, -6.6905e-05, 1)'
    >>> str(Colour.NewFromYiq(0.5922, 0.45885,-0.05, 0.5))
    '(0.999902, 0.499955, -6.6905e-05, 0.5)'

    '''
    return Colour(Colour.YiqToRgb(y, i, q), 'rgb', alpha, wref)

  @staticmethod
  def NewFromYuv(y, u, v, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed YUV values.

    Parameters:
      :y:
        The Y component value [0...1]
      :u:
        The U component value [-0.436...0.436]
      :v:
        The V component value [-0.615...0.615]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromYuv(0.5925, -0.2916, 0.3575))
    '(0.999989, 0.500015, -6.3276e-05, 1)'
    >>> str(Colour.NewFromYuv(0.5925, -0.2916, 0.3575, 0.5))
    '(0.999989, 0.500015, -6.3276e-05, 0.5)'

    '''
    return Colour(Colour.YuvToRgb(y, u, v), 'rgb', alpha, wref)

  @staticmethod
  def NewFromXyz(x, y, z, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed CIE-XYZ values.

    Parameters:
      :x:
        The Red component value [0...1]
      :y:
        The Green component value [0...1]
      :z:
        The Blue component value [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromXyz(0.488941, 0.365682, 0.0448137))
    '(1, 0.5, 6.81883e-08, 1)'
    >>> str(Colour.NewFromXyz(0.488941, 0.365682, 0.0448137, 0.5))
    '(1, 0.5, 6.81883e-08, 0.5)'

    '''
    return Colour(Colour.XyzToRgb(x, y, z), 'rgb', alpha, wref)

  @staticmethod
  def NewFromLab(l, a, b, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed CIE-LAB values.

    Parameters:
      :l:
        The L component [0...100]
      :a:
        The a component [-1...1]
      :b:
        The a component [-1...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromLab(66.9518, 0.43084, 0.739692))
    '(1, 0.5, 1.09491e-08, 1)'
    >>> str(Colour.NewFromLab(66.9518, 0.43084, 0.739692, wref=Colour.WHITE_REFERENCE['std_D50']))
    '(1.01238, 0.492011, -0.14311, 1)'
    >>> str(Colour.NewFromLab(66.9518, 0.43084, 0.739692, 0.5))
    '(1, 0.5, 1.09491e-08, 0.5)'
    >>> str(Colour.NewFromLab(66.9518, 0.43084, 0.739692, 0.5, Colour.WHITE_REFERENCE['std_D50']))
    '(1.01238, 0.492011, -0.14311, 0.5)'

    '''
    return Colour(Colour.XyzToRgb(*Colour.LabToXyz(l, a, b, wref)), 'rgb', alpha, wref)

  @staticmethod
  def NewFromCmy(c, m, y, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed CMY values.

    Parameters:
      :c:
        The Cyan component value [0...1]
      :m:
        The Magenta component value [0...1]
      :y:
        The Yellow component value [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromCmy(0, 0.5, 1)
    (1, 0.5, 0, 1.0)
    >>> Colour.NewFromCmy(0, 0.5, 1, 0.5)
    (1, 0.5, 0, 0.5)

    '''
    return Colour(Colour.CmyToRgb(c, m, y), 'rgb', alpha, wref)

  @staticmethod
  def NewFromCmyk(c, m, y, k, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed CMYK values.

    Parameters:
      :c:
        The Cyan component value [0...1]
      :m:
        The Magenta component value [0...1]
      :y:
        The Yellow component value [0...1]
      :k:
        The Black component value [0...1]
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromCmyk(1, 0.32, 0, 0.5))
    '(0, 0.34, 0.5, 1)'
    >>> str(Colour.NewFromCmyk(1, 0.32, 0, 0.5, 0.5))
    '(0, 0.34, 0.5, 0.5)'

    '''
    return Colour(Colour.CmyToRgb(*Colour.CmykToCmy(c, m, y, k)), 'rgb', alpha, wref)

  @staticmethod
  def NewFromHtml(html, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed HTML Colour definition.

    Parameters:
      :html:
        The HTML definition of the Colour (#RRGGBB or #RGB or a Colour name).
      :alpha:
        The Colour transparency [0...1], default is opaque.
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromHtml('#ff8000'))
    '(1, 0.501961, 0, 1)'
    >>> str(Colour.NewFromHtml('ff8000'))
    '(1, 0.501961, 0, 1)'
    >>> str(Colour.NewFromHtml('#f60'))
    '(1, 0.4, 0, 1)'
    >>> str(Colour.NewFromHtml('f60'))
    '(1, 0.4, 0, 1)'
    >>> str(Colour.NewFromHtml('lemonchiffon'))
    '(1, 0.980392, 0.803922, 1)'
    >>> str(Colour.NewFromHtml('#ff8000', 0.5))
    '(1, 0.501961, 0, 0.5)'

    '''
    return Colour(Colour.HtmlToRgb(html), 'rgb', alpha, wref)

  @staticmethod
  def NewFromPil(pil, alpha=1.0, wref=_DEFAULT_WREF):
    '''Create a new instance based on the specifed PIL Colour.

    Parameters:
      :pil:
        A PIL compatible Colour representation (0xBBGGRR)
      :alpha:
        The Colour transparency [0...1], default is opaque
      :wref:
        The whitepoint reference, default is 2° D65.

    Returns:
      A grapefruit.Colour instance.

    >>> str(Colour.NewFromPil(0x0080ff))
    '(1, 0.501961, 0, 1)'
    >>> str(Colour.NewFromPil(0x0080ff, 0.5))
    '(1, 0.501961, 0, 0.5)'

    '''
    return Colour(Colour.PilToRgb(pil), 'rgb', alpha, wref)

  def __GetAlpha(self):
    return self.__a
  alpha = property(fget=__GetAlpha, doc='The transparency of this Colour. 0.0 is transparent and 1.0 is fully opaque.')

  def __GetWRef(self):
    return self.__wref
  whiteRef = property(fget=__GetWRef, doc='the white reference point of this Colour.')

  def __GetRGB(self):
    return self.__rgb
  rgb = property(fget=__GetRGB, doc='The RGB values of this Colour.')

  def __GetHue(self):
    return self.__hsl[0]
  hue = property(fget=__GetHue, doc='The hue of this Colour.')

  def __GetHSL(self):
    return self.__hsl
  hsl = property(fget=__GetHSL, doc='The HSL values of this Colour.')

  def __GetHSV(self):
    h, s, v = Colour.RgbToHsv(*self.__rgb)
    return (self.__hsl[0], s, v)
  hsv = property(fget=__GetHSV, doc='The HSV values of this Colour.')

  def __GetYIQ(self):
    return Colour.RgbToYiq(*self.__rgb)
  yiq = property(fget=__GetYIQ, doc='The YIQ values of this Colour.')

  def __GetYUV(self):
    return Colour.RgbToYuv(*self.__rgb)
  yuv = property(fget=__GetYUV, doc='The YUV values of this Colour.')

  def __GetXYZ(self):
    return Colour.RgbToXyz(*self.__rgb)
  xyz = property(fget=__GetXYZ, doc='The CIE-XYZ values of this Colour.')

  def __GetLAB(self):
    return Colour.XyzToLab(wref=self.__wref, *Colour.RgbToXyz(*self.__rgb))
  lab = property(fget=__GetLAB, doc='The CIE-LAB values of this Colour.')

  def __GetCMY(self):
    return Colour.RgbToCmy(*self.__rgb)
  cmy = property(fget=__GetCMY, doc='The CMY values of this Colour.')

  def __GetCMYK(self):
    return Colour.CmyToCmyk(*Colour.RgbToCmy(*self.__rgb))
  cmyk = property(fget=__GetCMYK, doc='The CMYK values of this Colour.')

  def __GetIntTuple(self):
    return Colour.RgbToIntTuple(*self.__rgb)
  intTuple = property(fget=__GetIntTuple, doc='This Colour as a tuple of integers in the range [0...255]')

  def __GetHTML(self):
    return Colour.RgbToHtml(*self.__rgb)
  html = property(fget=__GetHTML, doc='This Colour as an HTML Colour definition.')

  def __GetPIL(self):
    return Colour.RgbToPil(*self.__rgb)
  pil = property(fget=__GetPIL, doc='This Colour as a PIL compatible value.')

  def __GetwebSafe(self):
    return Colour.RgbToWebSafe(*self.__rgb)
  webSafe = property(fget=__GetwebSafe, doc='The web safe Colour nearest to this one (RGB).')

  def __GetGreyscale(self):
    return Colour.RgbToGreyscale(*self.rgb)
  greyscale = property(fget=__GetGreyscale, doc='The greyscale equivalent to this Colour (RGB).')

  def ColourWithAlpha(self, alpha):
    '''Create a new instance based on this one with a new alpha value.

    Parameters:
      :alpha:
        The transparency of the new Colour [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromRgb(1.0, 0.5, 0.0, 1.0).ColourWithAlpha(0.5)
    (1.0, 0.5, 0.0, 0.5)

    '''
    return Colour(self.__rgb, 'rgb', alpha, self.__wref)

  def ColourWithWhiteRef(self, wref, labAsRef=False):
    '''Create a new instance based on this one with a new white reference.

    Parameters:
      :wref:
        The whitepoint reference.
      :labAsRef:
        If True, the L*a*b* values of the current instance are used as reference
        for the new Colour; otherwise, the RGB values are used as reference.

    Returns:
      A grapefruit.Colour instance.


    >>> c = Colour.NewFromRgb(1.0, 0.5, 0.0, 1.0, Colour.WHITE_REFERENCE['std_D65'])

    >>> c2 = c.ColourWithWhiteRef(Colour.WHITE_REFERENCE['sup_D50'])
    >>> c2.rgb
    (1.0, 0.5, 0.0)
    >>> '(%g, %g, %g)' % c2.whiteRef
    '(0.96721, 1, 0.81428)'

    >>> c2 = c.ColourWithWhiteRef(Colour.WHITE_REFERENCE['sup_D50'], labAsRef=True)
    >>> '(%g, %g, %g)' % c2.rgb
    '(1.01463, 0.490339, -0.148131)'
    >>> '(%g, %g, %g)' % c2.whiteRef
    '(0.96721, 1, 0.81428)'
    >>> '(%g, %g, %g)' % c.lab
    '(66.9518, 0.43084, 0.739692)'
    >>> '(%g, %g, %g)' % c2.lab
    '(66.9518, 0.43084, 0.739693)'

    '''
    if labAsRef:
      l, a, b = self.__GetLAB()
      return Colour.NewFromLab(l, a, b, self.__a, wref)
    else:
      return Colour(self.__rgb, 'rgb', self.__a, wref)

  def ColourWithHue(self, hue):
    '''Create a new instance based on this one with a new hue.

    Parameters:
      :hue:
        The hue of the new Colour [0...360].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5).ColourWithHue(60)
    (1.0, 1.0, 0.0, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5).ColourWithHue(60).hsl
    (60, 1, 0.5)

    '''
    h, s, l = self.__hsl
    return Colour((hue, s, l), 'hsl', self.__a, self.__wref)

  def ColourWithSaturation(self, saturation):
    '''Create a new instance based on this one with a new saturation value.

    .. note::

       The saturation is defined for the HSL mode.

    Parameters:
      :saturation:
        The saturation of the new Colour [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5).ColourWithSaturation(0.5)
    (0.75, 0.5, 0.25, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5).ColourWithSaturation(0.5).hsl
    (30, 0.5, 0.5)

    '''
    h, s, l = self.__hsl
    return Colour((h, saturation, l), 'hsl', self.__a, self.__wref)

  def ColourWithLightness(self, lightness):
    '''Create a new instance based on this one with a new lightness value.

    Parameters:
      :lightness:
        The lightness of the new Colour [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5).ColourWithLightness(0.25)
    (0.5, 0.25, 0.0, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5).ColourWithLightness(0.25).hsl
    (30, 1, 0.25)

    '''
    h, s, l = self.__hsl
    return Colour((h, s, lightness), 'hsl', self.__a, self.__wref)

  def DarkerColour(self, level):
    '''Create a new instance based on this one but darker.

    Parameters:
      :level:
        The amount by which the Colour should be darkened to produce
        the new one [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5).DarkerColour(0.25)
    (0.5, 0.25, 0.0, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5).DarkerColour(0.25).hsl
    (30, 1, 0.25)

    '''
    h, s, l = self.__hsl
    return Colour((h, s, max(l - level, 0)), 'hsl', self.__a, self.__wref)

  def LighterColour(self, level):
    '''Create a new instance based on this one but lighter.

    Parameters:
      :level:
        The amount by which the Colour should be lightened to produce
        the new one [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5).LighterColour(0.25)
    (1.0, 0.75, 0.5, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5).LighterColour(0.25).hsl
    (30, 1, 0.75)

    '''
    h, s, l = self.__hsl
    return Colour((h, s, min(l + level, 1)), 'hsl', self.__a, self.__wref)

  def Saturate(self, level):
    '''Create a new instance based on this one but more saturated.

    Parameters:
      :level:
        The amount by which the Colour should be saturated to produce
        the new one [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 0.5, 0.5).Saturate(0.25)
    (0.875, 0.5, 0.125, 1.0)
    >>> Colour.NewFromHsl(30, 0.5, 0.5).Saturate(0.25).hsl
    (30, 0.75, 0.5)

    '''
    h, s, l = self.__hsl
    return Colour((h, min(s + level, 1), l), 'hsl', self.__a, self.__wref)

  def Desaturate(self, level):
    '''Create a new instance based on this one but less saturated.

    Parameters:
      :level:
        The amount by which the Colour should be desaturated to produce
        the new one [0...1].

    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 0.5, 0.5).Desaturate(0.25)
    (0.625, 0.5, 0.375, 1.0)
    >>> Colour.NewFromHsl(30, 0.5, 0.5).Desaturate(0.25).hsl
    (30, 0.25, 0.5)

    '''
    h, s, l = self.__hsl
    return Colour((h, max(s - level, 0), l), 'hsl', self.__a, self.__wref)

  def WebSafeDither(self):
    '''Return the two websafe Colours nearest to this one.

    Returns:
      A tuple of two grapefruit.Colour instances which are the two
      web safe Colours closest this one.

    >>> c = Colour.NewFromRgb(1.0, 0.45, 0.0)
    >>> c1, c2 = c.WebSafeDither()
    >>> str(c1)
    '(1, 0.4, 0, 1)'
    >>> str(c2)
    '(1, 0.6, 0, 1)'

    '''
    return (
      Colour(Colour.RgbToWebSafe(*self.__rgb), 'rgb', self.__a, self.__wref),
      Colour(Colour.RgbToWebSafe(alt=True, *self.__rgb), 'rgb', self.__a, self.__wref))

  def Gradient(self, target, steps=100):
    '''Create a list with the gradient Colours between this and the other Colour.

    Parameters:
      :target:
        The grapefruit.Colour at the other end of the gradient.
      :steps:
        The number of gradients steps to create.


    Returns:
      A list of grapefruit.Colour instances.

    >>> c1 = Colour.NewFromRgb(1.0, 0.0, 0.0, alpha=1)
    >>> c2 = Colour.NewFromRgb(0.0, 1.0, 0.0, alpha=0)
    >>> c1.Gradient(c2, 3)
    [(0.75, 0.25, 0.0, 0.75), (0.5, 0.5, 0.0, 0.5), (0.25, 0.75, 0.0, 0.25)]

    '''
    gradient = []
    rgba1 = self.__rgb + (self.__a,)
    rgba2 = target.__rgb + (target.__a,)

    steps += 1
    for n in range(1, steps):
      d = 1.0*n/steps
      r = (rgba1[0]*(1-d)) + (rgba2[0]*d)
      g = (rgba1[1]*(1-d)) + (rgba2[1]*d)
      b = (rgba1[2]*(1-d)) + (rgba2[2]*d)
      a = (rgba1[3]*(1-d)) + (rgba2[3]*d)

      gradient.append(Colour((r, g, b), 'rgb', a, self.__wref))

    return gradient

  def ComplementaryColour(self, mode='ryb'):
    '''Create a new instance which is the complementary Colour of this one.

    Parameters:
      :mode:
        Select which Colour wheel to use for the generation (ryb/rgb).


    Returns:
      A grapefruit.Colour instance.

    >>> Colour.NewFromHsl(30, 1, 0.5).ComplementaryColour(mode='rgb')
    (0.0, 0.5, 1.0, 1.0)
    >>> Colour.NewFromHsl(30, 1, 0.5).ComplementaryColour(mode='rgb').hsl
    (210, 1, 0.5)

    '''
    h, s, l = self.__hsl

    if mode == 'ryb': h = Colour.RgbToRyb(h)
    h = (h+180)%360
    if mode == 'ryb': h = Colour.RybToRgb(h)

    return Colour((h, s, l), 'hsl', self.__a, self.__wref)

  def MonochromeScheme(self):
    '''Return 4 Colours in the same hue with varying saturation/lightness.

    Returns:
      A tuple of 4 grapefruit.Colour in the same hue as this one,
      with varying saturation/lightness.

    >>> c = Colour.NewFromHsl(30, 0.5, 0.5)
    >>> ['(%g, %g, %g)' % clr.hsl for clr in c.MonochromeScheme()]
    ['(30, 0.2, 0.8)', '(30, 0.5, 0.3)', '(30, 0.2, 0.6)', '(30, 0.5, 0.8)']

    '''
    def _wrap(x, min, thres, plus):
      if (x-min) < thres: return x + plus
      else: return x-min

    h, s, l = self.__hsl

    s1 = _wrap(s, 0.3, 0.1, 0.3)
    l1 = _wrap(l, 0.5, 0.2, 0.3)

    s2 = s
    l2 = _wrap(l, 0.2, 0.2, 0.6)

    s3 = s1
    l3 = max(0.2, l + (1-l)*0.2)

    s4 = s
    l4 = _wrap(l, 0.5, 0.2, 0.3)

    return (
      Colour((h, s1,  l1), 'hsl', self.__a, self.__wref),
      Colour((h, s2,  l2), 'hsl', self.__a, self.__wref),
      Colour((h, s3,  l3), 'hsl', self.__a, self.__wref),
      Colour((h, s4,  l4), 'hsl', self.__a, self.__wref))

  def TriadicScheme(self, angle=120, mode='ryb'):
    '''Return two Colours forming a triad or a split complementary with this one.

    Parameters:
      :angle:
        The angle between the hues of the created Colours.
        The default value makes a triad.
      :mode:
        Select which Colour wheel to use for the generation (ryb/rgb).

    Returns:
      A tuple of two grapefruit.Colour forming a Colour triad with
      this one or a split complementary.

    >>> c1 = Colour.NewFromHsl(30, 1, 0.5)

    >>> c2, c3 = c1.TriadicScheme(mode='rgb')
    >>> c2.hsl
    (150.0, 1, 0.5)
    >>> c3.hsl
    (270.0, 1, 0.5)

    >>> c2, c3 = c1.TriadicScheme(angle=40, mode='rgb')
    >>> c2.hsl
    (190.0, 1, 0.5)
    >>> c3.hsl
    (230.0, 1, 0.5)

    '''
    h, s, l = self.__hsl
    angle = min(angle, 120) / 2.0

    if mode == 'ryb': h = Colour.RgbToRyb(h)
    h += 180
    h1 = (h - angle) % 360
    h2 = (h + angle) % 360
    if mode == 'ryb':
      h1 = Colour.RybToRgb(h1)
      h2 = Colour.RybToRgb(h2)

    return (
      Colour((h1, s,  l), 'hsl', self.__a, self.__wref),
      Colour((h2, s,  l), 'hsl', self.__a, self.__wref))

  def TetradicScheme(self, angle=30, mode='ryb'):
    '''Return three Colours froming a tetrad with this one.

    Parameters:
      :angle:
        The angle to substract from the adjacent Colours hues [-90...90].
        You can use an angle of zero to generate a square tetrad.
      :mode:
        Select which Colour wheel to use for the generation (ryb/rgb).

    Returns:
      A tuple of three grapefruit.Colour forming a Colour tetrad with
      this one.

    >>> col = Colour.NewFromHsl(30, 1, 0.5)
    >>> [c.hsl for c in col.TetradicScheme(mode='rgb', angle=30)]
    [(90, 1, 0.5), (210, 1, 0.5), (270, 1, 0.5)]

    '''
    h, s, l = self.__hsl

    if mode == 'ryb': h = Colour.RgbToRyb(h)
    h1 = (h + 90 - angle) % 360
    h2 = (h + 180) % 360
    h3 = (h + 270 - angle) % 360
    if mode == 'ryb':
      h1 = Colour.RybToRgb(h1)
      h2 = Colour.RybToRgb(h2)
      h3 = Colour.RybToRgb(h3)

    return (
      Colour((h1, s,  l), 'hsl', self.__a, self.__wref),
      Colour((h2, s,  l), 'hsl', self.__a, self.__wref),
      Colour((h3, s,  l), 'hsl', self.__a, self.__wref))

  def AnalogousScheme(self, angle=30, mode='ryb'):
    '''Return two Colours analogous to this one.

    Args:
      :angle:
        The angle between the hues of the created Colours and this one.
      :mode:
        Select which Colour wheel to use for the generation (ryb/rgb).

    Returns:
      A tuple of grapefruit.Colours analogous to this one.

    >>> c1 = Colour.NewFromHsl(30, 1, 0.5)

    >>> c2, c3 = c1.AnalogousScheme(angle=60, mode='rgb')
    >>> c2.hsl
    (330, 1, 0.5)
    >>> c3.hsl
    (90, 1, 0.5)

    >>> c2, c3 = c1.AnalogousScheme(angle=10, mode='rgb')
    >>> c2.hsl
    (20, 1, 0.5)
    >>> c3.hsl
    (40, 1, 0.5)

    '''
    h, s, l = self.__hsl

    if mode == 'ryb': h = Colour.RgbToRyb(h)
    h += 360
    h1 = (h - angle) % 360
    h2 = (h + angle) % 360
    if mode == 'ryb':
      h1 = Colour.RybToRgb(h1)
      h2 = Colour.RybToRgb(h2)

    return (Colour((h1, s,  l), 'hsl', self.__a, self.__wref),
        Colour((h2, s,  l), 'hsl', self.__a, self.__wref))

  def AlphaBlend(self, other):
    '''Alpha-blend this Colour on the other one.

    Args:
      :other:
        The grapefruit.Colour to alpha-blend with this one.

    Returns:
      A grapefruit.Colour instance which is the result of alpha-blending
      this Colour on the other one.

    >>> c1 = Colour.NewFromRgb(1, 0.5, 0, 0.2)
    >>> c2 = Colour.NewFromRgb(1, 1, 1, 0.8)
    >>> c3 = c1.AlphaBlend(c2)
    >>> str(c3)
    '(1, 0.875, 0.75, 0.84)'

    '''
    # get final alpha channel
    fa = self.__a + other.__a - (self.__a * other.__a)

    # get percentage of source alpha compared to final alpha
    if fa==0: sa = 0
    else: sa = min(1.0, self.__a/other.__a)

    # destination percentage is just the additive inverse
    da = 1.0 - sa

    sr, sg, sb = [v * sa for v in self.__rgb]
    dr, dg, db = [v * da for v in other.__rgb]

    return Colour((sr+dr, sg+dg, sb+db), 'rgb', fa, self.__wref)

  def Blend(self, other, percent=0.5):
    '''Blend this Colour with the other one.

    Args:
      :other:
        the grapefruit.Colour to blend with this one.

    Returns:
      A grapefruit.Colour instance which is the result of blending
      this Colour on the other one.

    >>> c1 = Colour.NewFromRgb(1, 0.5, 0, 0.2)
    >>> c2 = Colour.NewFromRgb(1, 1, 1, 0.6)
    >>> c3 = c1.Blend(c2)
    >>> str(c3)
    '(1, 0.75, 0.5, 0.4)'

    '''
    dest = 1.0 - percent
    rgb = tuple(((u * percent) + (v * dest) for u, v in zip(self.__rgb, other.__rgb)))
    a = (self.__a * percent) + (other.__a * dest)
    return Colour(rgb, 'rgb', a, self.__wref)

def _test():
  import doctest
  reload(doctest)
  doctest.testmod()

if __name__=='__main__':
  _test()

# vim: ts=2 sts=2 sw=2 et
