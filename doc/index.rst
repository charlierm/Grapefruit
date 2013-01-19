.. _grapefruit-index:

.. image:: _static/GrapeFruit.png

Welcome! This is the documentation for GrapeFruit |release|, 
last updated |today|.

See the :ref:`genindex` for a list of the topics.


.. module:: grapefruit
.. moduleauthor:: Xavier Basty <xbasty@gmail.com>

==========================
The Colour class
==========================

.. class:: Colour

The grapefruit module contains only the :class:`Colour` class, which exposes all
the functionnalities. It can be used to store a Colour value and manipulate it,
or convert it to another Colour system.

If you are only interested in converting you Colours from one system to another,
you can store them using regular tuples instead of :class:`Colour` instances.
You can then use the class static methods to perform the conversions.

:class:`Colour` stores both the RGB and HSL representation of the Colour.
This makes possible to keep the hue intact when the Colour is a pure white
due to its lightness.
However, certain operations work only with the RGB values, and might then
lose the hue.

All the operations assume that you provide values in the specified ranges,
no checks are made whatsoever. If you provide a value outside of the
specified ranges, you'll get some strange results...

The class instances are immutable, all the methods return a new instance
of the :class:`Colour` class, and all the properties are read-only.

.. note::

   Some operations may provide results a bit outside the specified ranges,
   the results are not capped.
   This is due to certain Colour systems having a widers gamut than others.


Class content
---------------

- :ref:`class-constants`

  - :const:`Colour.WHITE_REFERENCE`
  - :const:`Colour.NAMED_Colour`

- :ref:`conversion-functions`

  - :meth:`Colour.RgbToHsl`
  - :meth:`Colour.HslToRgb`
  - :meth:`Colour.RgbToHsv`
  - :meth:`Colour.HsvToRgb`
  - :meth:`Colour.RgbToYiq`
  - :meth:`Colour.YiqToRgb`
  - :meth:`Colour.RgbToYuv`
  - :meth:`Colour.YuvToRgb`
  - :meth:`Colour.RgbToXyz`
  - :meth:`Colour.XyzToRgb`
  - :meth:`Colour.XyzToLab`
  - :meth:`Colour.LabToXyz`
  - :meth:`Colour.CmykToCmy`
  - :meth:`Colour.CmyToCmyk`
  - :meth:`Colour.RgbToCmy`
  - :meth:`Colour.CmyToRgb`
  - :meth:`Colour.RgbToHtml`
  - :meth:`Colour.HtmlToRgb`
  - :meth:`Colour.RgbToPil`
  - :meth:`Colour.PilToRgb`
  - :meth:`Colour.RgbToWebSafe`
  - :meth:`Colour.RgbToGreyscale`
  - :meth:`Colour.RgbToRyb`
  - :meth:`Colour.RybToRgb`

- :ref:`instantiation-functions`

  - :meth:`Colour.NewFromRgb`
  - :meth:`Colour.NewFromHsl`
  - :meth:`Colour.NewFromHsv`
  - :meth:`Colour.NewFromYiq`
  - :meth:`Colour.NewFromYuv`
  - :meth:`Colour.NewFromXyz`
  - :meth:`Colour.NewFromLab`
  - :meth:`Colour.NewFromCmy`
  - :meth:`Colour.NewFromCmyk`
  - :meth:`Colour.NewFromHtml`
  - :meth:`Colour.NewFromPil`

- :ref:`properties`

  - :attr:`Colour.alpha`
  - :attr:`Colour.whiteRef`
  - :attr:`Colour.rgb`
  - :attr:`Colour.hue`
  - :attr:`Colour.hsl`
  - :attr:`Colour.hsv`
  - :attr:`Colour.yiq`
  - :attr:`Colour.yuv`
  - :attr:`Colour.xyz`
  - :attr:`Colour.lab`
  - :attr:`Colour.cmy`
  - :attr:`Colour.cmyk`
  - :attr:`Colour.html`
  - :attr:`Colour.pil`
  - :attr:`Colour.webSafe`
  - :attr:`Colour.greyscale`

- :ref:`manipulation-methods`

  - :meth:`Colour.ColourWithAlpha`
  - :meth:`Colour.ColourWithWhiteRef`
  - :meth:`Colour.ColourWithHue`
  - :meth:`Colour.ColourWithSaturation`
  - :meth:`Colour.ColourWithLightness`
  - :meth:`Colour.DarkerColour`
  - :meth:`Colour.LighterColour`
  - :meth:`Colour.Saturate`
  - :meth:`Colour.Desaturate`
  - :meth:`Colour.WebSafeDither`

- :ref:`generation-methods`

  - :meth:`Colour.Gradient`
  - :meth:`Colour.ComplementaryColour`
  - :meth:`Colour.TriadicScheme`
  - :meth:`Colour.TetradicScheme`
  - :meth:`Colour.AnalogousScheme`

- :ref:`blending-methods`

  - :meth:`Colour.AlphaBlend`
  - :meth:`Colour.Blend`


Example usage
---------------

  To create an instance of the grapefruit.Colour from RGB values:
  
    >>> import grapefruit
    >>> r, g, b = 1, 0.5, 0
    >>> col = grapefruit.Colour.NewFromRgb(r, g, b)
  
  To get the values of the Colour in another Colourspace:
  
    >>> h, s, v = col.hsv
    >>> l, a, b = col.lab
  
  To get the complementary of a Colour:
  
    >>> compl = col.ComplementaryColour()
    >>> print compl.hsl
    (210.0, 1.0, 0.5)
  
  To directly convert RGB values to their HSL equivalent:
  
    >>> h, s, l = Colour.RgbToHsl(r, g, b)



.. _class-constants:

Class Constants
-----------------

.. data:: Colour.WHITE_REFERENCE

The reference white points of the CIE standards illuminants, calculated from
the chromaticity coordinates found at:
http://en.wikipedia.org/wiki/Standard_illuminant

A dictionary mapping the name of the CIE standard illuminants to their reference
white points. The white points are required for the XYZ <-> L*a*b conversions.

The key names are build using the following pattern: ``<observer>_<illuminant>``

The possible values for ``<observer>`` are:

  ======  ===================================
  Value   Observer
  ======  ===================================
  std     CIE 1931 2° Standard Observer
  sup     CIE 1964 10° Supplementary Observer
  ======  ===================================

The possible values for ``<illuminant>`` are the name of the standard illuminants:

  ======  ========  ==================================================
  Value   CCT       Illuminant
  ======  ========  ==================================================
  A       2856 K    Incandescent tungsten
  B       4874 K    Direct sunlight at noon (obsolete)
  C       6774 K    North sky daylight (obsolete)
  D50     5003 K    ICC Profile PCS. Horizon light.
  D55     5503 K    Compromise between incandescent and daylight
  D65     6504 K    Noon daylight (TV & sRGB Colourspace)
  D75     7504 K    North sky day light
  E       ~5455 K   Equal energy radiator (not a black body)
  F1      6430 K    Daylight Fluorescent
  F2      4230 K    Cool White Fluorescent
  F3      3450 K    White Fluorescent
  F4      2940 K    Warm White Fluorescent
  F5      6350 K    Daylight Fluorescent
  F6      4150 K    Lite White Fluorescent
  F7      6500 K    Broadband fluorescent, D65 simulator
  F8      5000 K    Broadband fluorescent, D50 simulator
  F9      4150 K    Broadband fluorescent, Cool White Deluxe
  F10     5000 K    Narrowband fluorescent, Philips TL85, Ultralume 50
  F11     4000 K    Narrowband fluorescent, Philips TL84, Ultralume 40
  F12     3000 K    Narrowband fluorescent, Philips TL83, Ultralume 30
  ======  ========  ==================================================

.. data:: Colour.NAMED_Colour

The names and RGB values of the X11 Colours supported by popular browsers, with
the gray/grey spelling issues, fixed so that both work (e.g light*grey* and
light*gray*).

Note: For *Gray*, *Green*, *Maroon* and *Purple*, the HTML/CSS values are used
instead of the X11 ones
(see `X11/CSS clashes <http://en.wikipedia.org/wiki/X11_Colour_names#Colour_names_that_clash_between_X11_and_HTML.2FCSS>`_)

Reference: `CSS3 Colour module <http://www.w3.org/TR/css3-iccprof#x11-Colour>`_


.. _conversion-functions:

Conversion functions
--------------------

The conversion functions are static methods of the :class:`Colour` class that
let you convert a Colour stored as the list of its components rather than
as a :class:`Colour` instance.

.. automethod:: Colour.RgbToHsl

.. automethod:: Colour.HslToRgb

.. automethod:: Colour.RgbToHsv

.. automethod:: Colour.HsvToRgb

.. automethod:: Colour.RgbToYiq

.. automethod:: Colour.YiqToRgb

.. automethod:: Colour.RgbToYuv

.. automethod:: Colour.YuvToRgb

.. automethod:: Colour.RgbToXyz

.. automethod:: Colour.XyzToRgb

.. automethod:: Colour.XyzToLab

.. automethod:: Colour.LabToXyz

.. automethod:: Colour.CmykToCmy

.. automethod:: Colour.CmyToCmyk

.. automethod:: Colour.RgbToCmy

.. automethod:: Colour.CmyToRgb

.. automethod:: Colour.RgbToHtml

.. automethod:: Colour.HtmlToRgb

.. automethod:: Colour.RgbToPil

.. automethod:: Colour.PilToRgb

.. automethod:: Colour.RgbToWebSafe

.. automethod:: Colour.RgbToGreyscale

.. automethod:: Colour.RgbToRyb

.. automethod:: Colour.RybToRgb



.. _instantiation-functions:

Instantiation functions
-----------------------

The instantiation functions let you create a new instance of the :class:`Colour`
class from the Colour components using the Colour system of your choice.

.. automethod:: Colour.NewFromRgb

.. automethod:: Colour.NewFromHsl

.. automethod:: Colour.NewFromHsv

.. automethod:: Colour.NewFromYiq

.. automethod:: Colour.NewFromYuv

.. automethod:: Colour.NewFromXyz

.. automethod:: Colour.NewFromLab

.. automethod:: Colour.NewFromCmy

.. automethod:: Colour.NewFromCmyk

.. automethod:: Colour.NewFromHtml

.. automethod:: Colour.NewFromPil



.. _properties:

Properties
----------

The properties get the value of the instance in the specified Colour model.

The properties returning calculated values unless marked otherwise.

.. note::

   All the properties are read-only. You need to make a copy of the instance
   to modify the Colour value.

.. autoattribute:: Colour.alpha

  *This value is not calculated,  the stored value is returned directly.*

.. autoattribute:: Colour.whiteRef

  *This value is not calculated,  the stored value is returned directly.*

.. autoattribute:: Colour.rgb

  *This value is not calculated,  the stored value is returned directly.*

.. autoattribute:: Colour.hue

  *This value is not calculated,  the stored value is returned directly.*

.. autoattribute:: Colour.hsl

  *This value is not calculated,  the stored value is returned directly.*

.. autoattribute:: Colour.hsv

.. autoattribute:: Colour.yiq

.. autoattribute:: Colour.yuv

.. autoattribute:: Colour.xyz

.. autoattribute:: Colour.lab

.. autoattribute:: Colour.cmy

.. autoattribute:: Colour.cmyk

.. autoattribute:: Colour.html

.. autoattribute:: Colour.pil

.. autoattribute:: Colour.webSafe

.. attribute:: Colour.greyscale



.. _manipulation-methods:

Manipulation methods
--------------------

The manipulations methods let you create a new Colour by changing an existing
Colour properties.

.. note::

   The methods **do not** modify the current Colour instance. They create a
   new instance or a tuple of new instances with the specified modifications.

.. automethod:: Colour.ColourWithAlpha

.. automethod:: Colour.ColourWithWhiteRef

.. automethod:: Colour.ColourWithHue

.. automethod:: Colour.ColourWithSaturation

.. automethod:: Colour.ColourWithLightness

.. automethod:: Colour.DarkerColour

.. automethod:: Colour.LighterColour

.. automethod:: Colour.Saturate

.. automethod:: Colour.Desaturate

.. automethod:: Colour.WebSafeDither



.. _generation-methods:

Generation methods
------------------

The generation methods let you create a Colour scheme by using a Colour as the
start point.

All the method, appart from Gradient and MonochromeScheme, have a 'mode'
parameter that let you choose which Colour wheel should be used to generate
the scheme.

The following modes are available:
  :ryb:
    The `RYB <http://en.wikipedia.org/wiki/RYB_Colour_model>`_ Colour wheel,
    or *artistic Colour wheel*. While scientifically incorrect, it generally
    produces better schemes than RGB.
  :rgb:
    The standard RGB Colour wheel.

.. automethod:: Colour.Gradient

.. automethod:: Colour.ComplementaryColour

.. automethod:: Colour.MonochromeScheme

.. automethod:: Colour.TriadicScheme

.. automethod:: Colour.TetradicScheme

.. automethod:: Colour.AnalogousScheme



.. _blending-methods:

Blending methods
----------------

.. automethod:: Colour.AlphaBlend

.. automethod:: Colour.Blend
