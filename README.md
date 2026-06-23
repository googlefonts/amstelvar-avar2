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

### Blended axes

1. `opsz` Optical size
2. `wght` Weight
3. `wdth` Width
4. `XTSP` Proportional spacing

### Parametric axes

1. `WDSP` Word space width
2. `GRAD` None
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
18. `XQUC` X internal curvature uppercase
19. `YQUC` Y internal curvature uppercase
20. `XUCS` X sidebearing uppercase straights
21. `XUCR` X sidebearing uppercase rounds
22. `XUCD` X sidebearing uppercase diagonals
23. `XOLC` X stem lowercase
24. `YOLC` Y stem lowercase
25. `XOLA` Lowercase accents main weight
26. `YOLA` Lowercase accents secondary weight
27. `XTLC` X transparent lowercase
28. `XTLR` X transparent lowercase rounds
29. `XTLD` X transparent lowercase diagonals
30. `XTLA` Lowercase accent width
31. `YTLC` Y transparent lowercase
32. `YTAS` Y transparent ascender
33. `YTDE` Y transparent descender
34. `XSHL` X horizontal serif lowercase
35. `YSHL` Y horizontal serif lowercase
36. `XSVL` X vertical serif lowercase
37. `YSVL` Y vertical serif lowercase
38. `XQLC` X internal curvature lowercase
39. `YQLC` Y internal curvature lowercase
40. `XLCS` X sidebearing lowercase straights
41. `XLCR` X sidebearing lowercase rounds
42. `XLCD` X sidebearing lowercase diagonals
43. `XOFI` X stem figures
44. `YOFI` Y stem figures
45. `XTFI` X transparent figures
46. `YTFI` Y transparent figures
47. `XSHF` X horizontal serif figures
48. `YSHF` Y horizontal serif figures
49. `XSVF` X vertical serif figures
50. `YSVF` Y vertical serif figures
51. `XQFI` X internal curvature figures
52. `YQFI` Y internal curvature figures
53. `XFIR` X sidebearing figure 0
54. `XDOT` Dot width
55. `YTOS` Lowercase overshoot
56. `XTTW` Trap width
57. `YTTL` Trap length
58. `BARS` 

### Tuning axes

- `TN00` opsz144
- `TN01` opsz144 wdth125
- `TN02` opsz144 wdth50
- `TN03` opsz144 wght100
- `TN04` opsz144 wght1000
- `TN05` opsz144 wght1000 wdth125
- `TN06` opsz144 wght1000 wdth50
- `TN07` opsz144 wght100 wdth125
- `TN08` opsz144 wght100 wdth50
- `TN09` opsz8
- `TN10` opsz8 wdth125
- `TN11` opsz8 wdth50
- `TN12` opsz8 wght100
- `TN13` opsz8 wght1000
- `TN14` opsz8 wght1000 wdth125
- `TN15` opsz8 wght1000 wdth50
- `TN16` opsz8 wght100 wdth125
- `TN17` opsz8 wght100 wdth50
- `TN18` wdth125
- `TN19` wdth50
- `TN20` wght100
- `TN21` wght1000
- `TN22` wght1000 wdth125
- `TN23` wght1000 wdth50
- `TN24` wght100 wdth125
- `TN25` wght100 wdth50
