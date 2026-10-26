AmstelvarA2
===========

Alpha version of Amstelvar with avar2 data. (work in progress)

> [!WARNING]  
> *This repository is very large!* (5.3 GB)  
>
> Unless you need the full data set for analysis, we recommend doing a [blobless clone] to download only data files in the HEAD state:  
>
> `git clone --filter=blob:none git@github.com:googlefonts/amstelvar-avar2.git` 

[blobless clone]: http://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/


Folder structure
----------------

```
AmstelvarA2
├── Fonts/
├── Proofs/
├── Sources/
├── Tools/
├── OFL.txt
├── README.md
└── build.sh
```

<dl>
  <dt><a href='#fonts'>Fonts</a></dt>
  <dd>font binaries</dd>
  <dt><a href='#proofs'>Proofs</a></dt>
  <dd>proofs of sources and variable fonts</dd>
  <dt><a href='#sources'>Sources</a></dt>
  <dd>source files in editable format</dd>
  <dt><a href='#tools'>Tools</a></dt>
  <dd>scripts used during production</dd>
  <dt>build.sh</dt>
  <dd>shell script to build the fonts using <a href='http://github.com/googlefonts/fontmake'>fontmake</a></dd>
</dl>


Fonts
-----

```
Fonts
├── reference/
├── AmstelvarA2-Roman_avar2.ttf
└── AmstelvarA2-Italic_avar2.ttf
```

<dl>
<dt>reference</dt>
<dd>Subfolder containing the original avar1 version of Amstelvar for use in proofs.</dd>
<dt>AmstelvarA2-Roman_avar2.ttf, AmstelvarA2-Italic_avar2.ttf</dt>
<dd>Roman and Italic variable fonts in avar2 format (with tuning axes).</dd>
<dt>AmstelvarA2-Roman_avar2_no-tuning.ttf, AmstelvarA2-Italic_avar2_no-tuning.ttf</dt>
<dd>Roman and Italic variable fonts in avar2 format, without tuning axes (for file size comparison).</dd>
</dl>


Proofs
------

```
Proofs
├── HTML/
├── PDF/
└── fontra.txt
```

<dl>
  <dt>HTML</dt>
  <dd>Interactive proofs of the variable fonts in HTML/CSS/JS format.</dd>
  <dt>PDF</dt>
  <dd>Static proofs of sources and variable fonts in PDF format.</dd>
  <dt>fontra.txt</dt>
  <dd>Test text strings for previewing glyph sets in Fontra.</dd>
</dl>


Sources
-------

This folder contains two subfolders with separate files for Roman and Italic, and any project-level files which are used by both styles.

```
Sources
├── Italic/
└── Roman/
```

### Roman (+ same structure for Italic)

```
Roman
├── *.ufo
├── measurements.json
├── blends.json
├── AmstelvarA2-Roman.designspace
├── AmstelvarA2-Roman.roboFontSets
├── AmstelvarA2-Roman.glyphConstruction
├── features/
├── reference/
└── tuning/

```

<dl>
<dt>*.ufo</dt>
<dd>Font sources in UFO format, with files named according to their variation parameters.</dd>
<dt>measurements.json</dt>
<dd>Standalone JSON file containing definitions for various font- and glyph-level measurements.<br/>
  Created using the <a href='http://gferreira.github.io/xTools4/reference/tools/variable/measurements/'>Measurements tool</a>.<br/>
  See <a href='http://gferreira.github.io/xTools4/reference/measurements-format/'>Measurements format</a> for documentation of the data format.</dd>
<dt>blends.json</dt>
<dd>Standalone JSON file containing definitions of blended axes and blended sources from parametric axes.<br/>
  Used when building the avar2 designspace.</dd>
<dt>AmstelvarA2-Roman_avar2.designspace</dt>
<dd>Designspace for building the avar2 variable font.</dd>
<dt>features</dt>
<dd>Subfolder with .fea files containing OpenType feature code used by the source fonts.</dd>
<dt>AmstelvarA2-Roman.roboFontSets</dt>
<dd><a href='http://robofont.com/documentation/topics/smartsets/'>SmartSets</a> file containing various sets of glyphs.</dd>
<dt>AmstelvarA2-Roman.glyphConstruction</dt>
<dd><a href='https://github.com/typemytype/GlyphConstruction'>GlyphConstruction</a> file containing instructions for building glyphs from components.</dd>
<dt>reference</dt>
<dd>Subfolder with .ufo reference sources, one for each corner of the opsz/wght/wdth designspace.<br/>
The original Amstelvar sources were changed for full compatibility with AmstelvarA2 sources.
</dd>
<dt>tuning</dt>
<dd>Subfolder with .ufo tuning sources, one for each corner of the opsz/wght/wdth designspace.<br/>
These sources are calculated automatically from parametric and reference sources.
</dd>

</dl>


Tools
-----

```
Tools
├── blending/
├── production/
├── proofing/
├── reference/
└── controller.py
```

### Project controller

The file `controller.py` contains the project controller, which is used to perform several tasks on the sources. 

<!-- The controller is a subclass of [xProject](http://gferreira.github.io/xTools4/explanations/xproject-overview/). -->

Tasks performed by the controller include:

- measuring and automatically naming UFO sources
- automatically building the designspace from source files
- blending typographic styles from parametric axes
- cleaning up and normalizing UFO sources
- copying data from the default to all other sources
- navigating and filtering the glyph set
- building and validating composite glyphs
- generating different kinds of PDF proofs
- building variable fonts and instances
- …and much more.

### Production scripts

A subfolder containing various scripts used during development.


Blending
--------

The maping values for blending `opsz` `wght` `wdth` from parametric axes are produced by measuring the original styles of Amstelvar, which are included in this repository as reference sources. 

The extracted measurements are stored in a `blends.json` file, which is processed by the AmstelvarA2 controller to build the designspace.


Tuning
------

Tuning sources are calculated automatically as the difference between parametric blends and reference sources.

Each tuning axis controls the deltas needed to tune one of 26 corners of the designspace. In locations in between these corners, the tuning deltas are linearly interpolated.


Variation axes
--------------

### Blended axes

1. `opsz` Optical size
2. `wght` Weight
3. `wdth` Width
4. `XTSP` Proportional spacing

### Parametric axes

1. `WDSP` Word space width
2. `GRAD` Grade
3. `XOUC` X stem uppercase
4. `YOUC` Y stem uppercase
5. `XOUA` Uppercase accents main weight
6. `YOUA` Uppercase accents secondary weight
7. `XTUC` X transparent uppercase
8. `XTUR` X transparent uppercase rounds
9. `XTUD` X transparent uppercase diagonals
10. `XTUA` Uppercase accent width
11. `YTUC` Y transparent uppercase
12. `YTJD` Y transparent J descender
13. `XSHU` X horizontal serif uppercase
14. `YSHU` Y horizontal serif uppercase
15. `XSVU` X vertical serif uppercase
16. `YSVU` Y vertical serif uppercase
17. `XVAU` Uppercase vertical serif angle
18. `XUCS` X sidebearing uppercase straights
19. `XUCR` X sidebearing uppercase rounds
20. `XUCD` X sidebearing uppercase diagonals
21. `XOLC` X stem lowercase
22. `YOLC` Y stem lowercase
23. `XOLA` Lowercase accents main weight
24. `YOLA` Lowercase accents secondary weight
25. `XTLC` X transparent lowercase
26. `XTLR` X transparent lowercase rounds
27. `XTLD` X transparent lowercase diagonals
28. `XTLA` Lowercase accent width
29. `YTLC` Y transparent lowercase
30. `YTAS` Y transparent ascender
31. `YTDE` Y transparent descender
32. `XSHL` X horizontal serif lowercase
33. `YSHL` Y horizontal serif lowercase
34. `XSVL` X vertical serif lowercase
35. `YSVL` Y vertical serif lowercase
36. `XLCS` X sidebearing lowercase straights
37. `XLCR` X sidebearing lowercase rounds
38. `XLCD` X sidebearing lowercase diagonals
39. `XOFI` X stem figures
40. `YOFI` Y stem figures
41. `XTFI` X transparent figures
42. `YTFI` Y transparent figures
43. `XSHF` X horizontal serif figures
44. `YSHF` Y horizontal serif figures
45. `XSVF` X vertical serif figures
46. `YSVF` Y vertical serif figures
47. `XFIR` X sidebearing figures round
48. `XOET` X stem etcetera
49. `YOET` Y stem etcetera
50. `XTET` X transparent etcetera
51. `XETS` X sidebearing etcetera
52. `XDOT` Dot width
53. `YTOS` Lowercase overshoot
54. `XTTW` Trap width
55. `YTTL` Trap length
56. `BARS` Bars

### Tuning axes

1. `TN00` opsz144
2. `TN01` opsz144 wdth125
3. `TN02` opsz144 wdth50
4. `TN03` opsz144 wght100
5. `TN04` opsz144 wght1000
6. `TN05` opsz144 wght1000 wdth125
7. `TN06` opsz144 wght1000 wdth50
8. `TN07` opsz144 wght100 wdth125
9. `TN08` opsz144 wght100 wdth50
10. `TN09` opsz8
11. `TN10` opsz8 wdth125
12. `TN11` opsz8 wdth50
13. `TN12` opsz8 wght100
14. `TN13` opsz8 wght1000
15. `TN14` opsz8 wght1000 wdth125
16. `TN15` opsz8 wght1000 wdth50
17. `TN16` opsz8 wght100 wdth125
18. `TN17` opsz8 wght100 wdth50
19. `TN18` wdth125
20. `TN19` wdth50
21. `TN20` wght100
22. `TN21` wght1000
23. `TN22` wght1000 wdth125
24. `TN23` wght1000 wdth50
25. `TN24` wght100 wdth125
26. `TN25` wght100 wdth50