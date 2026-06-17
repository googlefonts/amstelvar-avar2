# test avar2 variable font in DrawBot

import os
from random import randint 

subFamily = ['Roman', 'Italic'][0]

folder  = os.path.dirname(os.path.dirname(os.getcwd()))
ttfPath = os.path.join(folder, 'Fonts', f'AmstelvarA2-{subFamily}_avar2.ttf')

print(ttfPath, os.path.exists(ttfPath))

newPage('A4')
font(ttfPath)

parameters = listFontVariations(ttfPath)
defaults = fontVariations()

sliders = []
for parameter in parameters.keys():
    slider = dict(name=parameter, ui="Slider", 
            args=dict(
                value=defaults[parameter],
                minValue=parameters[parameter]['minValue'],
                maxValue=parameters[parameter]['maxValue']
            )
        )
    sliders.append(slider)

lineHeightSlider = dict(name='lineheight', ui="Slider", args=dict(value=1.25, minValue=1.0, maxValue=1.5))
fontSizeSlider = dict(name='fontsize', ui="Slider", args=dict(value=18, minValue=9, maxValue=72))
sliders.insert(0, lineHeightSlider)
sliders.insert(0, fontSizeSlider)

Variable([slider for slider in sliders], globals())

p = 20
x = y = p
w = width() - p*2
h = height() - p*2

txt = '''OpenType variable fonts are an adaptation of Apple's TrueType GX font variations to OpenType, with integration into key aspects of the OpenType format including OpenType Layout tables and both TrueType and CFF glyph outline formats. It also surpasses TrueType GX by providing better interoperability, both between different fonts, and between variable fonts and font-formatting specifications such as those found in Cascading Style Sheets. The technology allows software to access any design instance for a continuous range of designs defined within the font. When a specific design instance has been selected, the glyph outlines or other data values for that design instance are computed as font data is being processed during text layout and rasterization. The technology uses interpolation and extrapolation mechanisms that have been supported in font-development tools and used by font designers for many years. In that paradigm, the font designer creates a variable design, but then chooses specific instances to generate as static, non-variable fonts that get distributed to customers. With variable fonts, however, the font produced and distributed by the font designer can have built-in variability, and the interpolation mechanisms can now be built into operating systems and Web browsers or other applications, with specific design instances selected at time of use. One of the key benefits of the technology is that it can significantly reduce the combined size of font data whenever multiple styles are in use. On the Web, this may allow a site to use more font styles while at the same time reducing page load times. A further benefit is that it gives access to a continuous range of style variations, which can provide benefits for responsive design.'''

variations = {}
for p in parameters:
    variations[p] = locals()[p]

T = FormattedString()
T.font(ttfPath)
T.fontSize(fontsize)
T.lineHeight(fontsize*lineheight)
T.fontVariations(**variations)
# T.openTypeFeatures(kern=False)
T.append(txt)

textBox(T, (x, y, w, h))
