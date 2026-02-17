AmstelvarA2
===========

Alpha version of Amstelvar with avar2 data. (work in progress)

> [!WARNING]  
> *This repository is very large!* (5.3 GB)  
>
> Unless you need the full data set for analysis, we recommend doing a [blobless clone] to download only data files in the HEAD state:  
>
> `git clone --filter=blob:none git@github.com:googlefonts/roboto-delta.git`

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
  <dd>font binaries for testing</dd>
  <dt><a href='#proofs'>Proofs</a></dt>
  <dd>proofs of the variable fonts</dd>
  <dt><a href='#sources'>Sources</a></dt>
  <dd>various source files used to design and build the variable fonts</dd>
  <dt><a href='#tools'>Tools</a></dt>
  <dd>scripts used during production</dd>
  <dt>build.sh</dt>
  <dd>shell script to build Roman & Italic variable fonts from their source files</dd>
</dl>


Fonts
-----

```
Fonts
├── legacy/
├── AmstelvarA2-Roman_avar2.ttf
└── AmstelvarA2-Italic_avar2.ttf
```

<dl>
<dt>legacy</dt>
<dd>Subfolder containing the original avar1 version of Amstelvar for use in proofs.</dd>
<dt>AmstelvarA2-Roman_avar2.ttf, AmstelvarA2-Italic_avar2.ttf</dt>
<dd>Roman and Italic variable fonts in avar2 format</dd>
</dl>


Proofs
------

```
Proofs
├── HTML/
├── PDF/
└── fontra-test-strings.txt
```

<dl>
  <dt>HTML</dt>
  <dd>Interactive proofs in HTML/CSS/JS format.</dd>
  <dt>PDF</dt>
  <dd>Static proofs in PDF format.</dd>
  <dt>fontra-test-strings.txt</dt>
  <dd>Test text strings for previewing glyph sets in Fontra.</dd>
</dl>


Sources
-------

This folder contains two subfolders with separate files for Roman and Italic, and project-level files which are used by both styles.

```
Sources
├── Italic/
├── Roman/
└── AmstelvarA2.roboFontSets
```

### Roman (+ same structure for Italic)

```
Roman
├── *.ufo
├── measurements.json
├── blends.json
├── features/*.fea
├── AmstelvarA2-Roman.glyphConstruction
├── AmstelvarA2-Roman.roboFontSets
└── AmstelvarA2-Roman_avar2.designspace
```

<dl>
<dt>*.ufo</dt>
<dd>Font sources in UFO format, with files named according to their variation parameters.</dd>
<dt>measurements.json</dt>
<dd>Standalone JSON file containing definitions for various font- and glyph-level measurements.<br/>
  Created using the <a href='http://gferreira.github.io/fb-variable-values/reference/measurements/'>Measurements tool</a> from the VariableValues RoboFont extension.<br/>
  See <a href='http://gferreira.github.io/fb-variable-values/reference/measurements-format/'>Measurements format</a> for documentation of the data format.</dd>
<dt>blends.json</dt>
<dd>Standalone JSON file containing definitions of blended axes and blended sources from parametric axes.<br/>
  Used when building the avar2 designspace.</dd>
<dt>features</dt>
<dd>Subfolder with .fea files containing OpenType feature code used by the source fonts.</dd>
<dt>AmstelvarA2-Roman.glyphConstruction</dt>
<dd><a href='https://github.com/typemytype/GlyphConstruction'>GlyphConstruction</a> file containing instructions for building glyphs from components.</dd>
<dt>AmstelvarA2-Roman.roboFontSets</dt>
<dd><a href='http://robofont.com/documentation/topics/smartsets/'>SmartSets</a> file containing various sets of glyphs.</dd>
<dt>AmstelvarA2-Roman_avar2.designspace
<dd>Designspace for building the avar2 variable font.</dd>
</dl>


Tools
-----

```
Tools
├── blending/
├── production/
├── proofing/
└── build-designspace.py
```

### Production scripts

A subfolder containing various scripts used during development. The most relevant ones are listed below.

<dl>
  <dt>set-names-from-measurements.py</dt>
  <dd>Set file name and style name from measurements in all UFOs in a given folder.<br/>
    Includes a preflight mode which only prints the new names without changing the files.</dd>
  <dt>copy-glyphs.py</dt>
  <dd>Copy glyphs from the default font to selected sources.</dd>
  <dt>build-glyphs.py</dt>
  <dd>Build glyphs from glyph constructions in the selected sources.</dd>
  <dt>validate-locations.py</dt>
  <dd>Check if source locations are within the allowed min/max bounds for each axis.<br/>
    Helpful when debugging calculated blend values in relation to the current parametric axes.</dd>
  <dt>mark-components.py</dt>
  <dd>Mark glyphs in the current font containing components with different colors depending on their components' nesting level.</dd>
</dl>


Blending
--------

The appropriate values for blending `opsz` `wght` `wdth` from parametric axes are produced on a [separate repository](http://github.com/gferreira/amstelvar) which is a fork of the original Amstelvar source. [The naming of UFO files was adjusted for easier parameter parsing (using underscores to separate parameters instead of hyphens), and all unnecessary files were deleted.]

A separate measurements file was added for Amstelvar, with the same parameters used for measuring AmstelvarA2. This file is needed because the contour structures of the two versions are different, and in most measurements different point indexes must be used.

### Extracting measurements

Using this separate measurements file, the original Amstelvar sources are then measured to produce the `blends.json` file which is used by the AmstelvarA2 designspace builder.


Variation axes in AmstelvarA2
-----------------------------

### Typographic axes

1. `opsz` Optical size
2. `wght` Weight
3. `wdth` Width
4. `XTSP` Proportional spacing

### Parametric axes

1. `WDSP` Word space width
2. `GRAD` Grades
3. `XOUC` X stem uppercase
4. `YOUC` Y stem uppercase
5. `XOUA` Uppercase accents main weight
6. `YOUA` Uppercase accents secondary weight
7. `XTUC` X transparent uppercase
8. `XTUR` X transparent uppercase rounds
9. `XTUD` X transparent uppercase diagonals
10. `XTUA` Uppercase accent width
11. `YTUC` Y transparent uppercase
12. `YTJD` None
13. `XSHU` X horizontal serif uppercase
14. `YSHU` Y horizontal serif uppercase
15. `XSVU` X vertical serif uppercase
16. `YSVU` Y vertical serif uppercase
17. `XVAU` Uppercase vertical serif angle
18. `YHAU` Uppercase horizontal serif angle
19. `XQUC` X internal curvature uppercase
20. `YQUC` Y internal curvature uppercase
21. `XUCS` X sidebearing uppercase straights
22. `XUCR` X sidebearing uppercase rounds
23. `XUCD` X sidebearing uppercase diagonals
24. `XOLC` X stem lowercase
25. `YOLC` Y stem lowercase
26. `XOLA` Lowercase accents main weight
27. `YOLA` Lowercase accents secondary weight
28. `XTLC` X transparent lowercase
29. `XTLR` X transparent lowercase rounds
30. `XTLD` X transparent lowercase diagonals
31. `XTLA` Lowercase accent width
32. `YTLC` Y transparent lowercase
33. `YTAS` Y transparent ascender
34. `YTDE` Y transparent descender
35. `XSHL` X horizontal serif lowercase
36. `YSHL` Y horizontal serif lowercase
37. `XSVL` X vertical serif lowercase
38. `YSVL` Y vertical serif lowercase
39. `XVAL` Lowercase vertical serif angle
40. `YHAL` Lowercase horizontal serif angle
41. `XLCS` X sidebearing lowercase straights
42. `XLCR` X sidebearing lowercase rounds
43. `XLCD` X sidebearing lowercase diagonals
44. `XQLC` X internal curvature lowercase
45. `YQLC` Y internal curvature lowercase
46. `XOFI` X stem figures
47. `YOFI` Y stem figures
48. `XTFI` X transparent figures
49. `YTFI` Y transparent figures
50. `XSHF` X horizontal serif figures
51. `YSHF` Y horizontal serif figures
52. `XSVF` X vertical serif figures
53. `YSVF` Y vertical serif figures
54. `XVAF` Figures vertical serif angle
55. `YHAF` Figures horizontal serif angle
56. `XFIR` X sidebearing figure 0
57. `XQFI` X internal curvature figures
58. `YQFI` Y internal curvature figures
59. `XDOT` Dot width
60. `YTOS` Lowercase overshoot
61. `XTTW` Trap width
62. `YTTL` Trap length
63. `BARS`
