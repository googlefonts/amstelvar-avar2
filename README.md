AmstelvarA2
===========

Alpha version of Amstelvar with avar2 data. (work in progress)


Folder structure
----------------

```
AmstelvarA2
├── Fonts/
├── Proofs/
├── Source/tools/
├── Source/
├── README.md
└── OFL.txt
```

<dl>
  <dt>Fonts</dt>
  <dd>contains font binaries for testing</dd>
  <dt>Proofs</dt>
  <dd>contains proofs of the variable fonts</dd>
  <dt>Source/tools</dt>
  <dd>contains Python scripts used during production</dd>
  <dt>Source</dt>
  <dd>contains various source files used to design and build the variable fonts</dd>
</dl>


Fonts
-----

```
Fonts
├── AmstelvarA2-Roman_avar1.ttf
└── AmstelvarA2-Roman_avar2.ttf
```

<dl>
  <dt>AmstelvarA2-Roman_avar1.ttf</dt>
  <dd>Variable font in avar1 format.<br/>
    Blended axes are created by instantiating their extrema from parametric axes, and inserting them into the designspace as sources.</dd>
  <dt>AmstelvarA2-Roman_avar2.ttf</dt>
  <dd>Variable font in avar2 format.<br/>
    Blended axes are created by defining mappings from parametric axes to extrema input values.</dd>
  <!--
  <dt>AmstelvarA2-Roman_avar2_fences.ttf</dt>
  <dd>Attempt to build an avar2 font with “fences” to restrict the limits of parametric values at blended extrema locations.<br/>
    ⚠️ <em>The added fences work at the default location, but not at the blended extrema.</em>*</dd>
  <dt>AmstelvarA2-Roman_avar2_fences-wght200.ttf</dt>
  <dd>Attempt to implement fences at one blended extreme only, for testing purposes.<br/>
    ⚠️ <em>The fences added for location <code>wght200</code> do not work as intended.</em>*</dd></dd>
  -->
</dl>

\* see [Implementing fences](https://github.com/googlefonts/amstelvar-avar2/issues/4)


Proofs
------

```
Proofs
├── avar2-avar1.html
├── avar2-original_blends.html
├── avar2-original_compare.html
├── compare-1.pdf
├── avar2-test.py
└── avar2-test-parameters.py
```

<dl>
  <dt>compare-1.pdf</dt>
  <dd>Screen grabs of comparison of Amstelvar 1.0 (avar) vs. Amstelvar2 (avar2) ASCII Prototype, at the same designspace locations.</dd>
  <dt>avar2-original_blends.html</dt>
  <dd>Interactive HTML page for comparison between AmstelvarA2 avar2 (parametric axes) and the original Amstelvar (opsz wght wdth).<br/>
    Useful when defining and checking parametric locations of blended extrema against their avar2 blends.</dd>
  <dt>avar2-original_compare.html</dt>
  <dd>Interactive HTML page for comparison between AmstelvarA2 avar2 and the original Amstelvar at the same location (opsz wght wdth).<br/>
    Useful to compare the new avar2 blends to the original avar font.</dd>
  <dt>avar2-avar1.html</dt>
  <dd>Interactive HTML page for comparison between avar2 and avar1 versions of AmstelvarA2.<br/>
    Useful as a reference when testing the avar2 implementation.</dd>
  <dt>avar2-test.py</dt>
  <dd>Interactive DrawBot script for testing the avar2 variable font using the native macOS text engine.<br/>
    Produces a PDF document.</dd>
  <dt>avar2-test-parameters.py</dt>
  <dd>An attempt to create a visualization of parametric values for changes in blended axes.<br/>
    ⚠️ <em>Not working because point indexes in the variable font are different from point indexes in the source UFOs. <strong>(double check!)</strong></em></dd>
</dl>


Source
-------

This folder contains two subfolders with separate files for Roman and Italic, and project-level files which are used by both styles, and a subfolder for tools.

```
Source
├── Italic/
├── Roman/
├── AmstelvarA2.roboFontSets
└── AmstelvarA2.glyphConstruction
```

<dl>
  <dt>AmstelvarA2.roboFontSets</dt>
  <dd><a href='http://robofont.com/documentation/topics/smartsets/'>SmartSets</a> file containing various sets of glyphs.<br/>
    Useful as UI feature when browsing complete fonts, and as a data format when writing scripts that apply only to certain sets of glyphs.</dd>
  <dt>AmstelvarA2.glyphConstruction</dt>
  <dd><a href='https://github.com/typemytype/GlyphConstruction'>GlyphConstruction</a> file containing instructions for building glyphs from components.</dd>
</dl>

### Roman

```
Roman
├── *.ufo
├── measurements.json
├── blends.json
├── fences.json
├── features
│   └── *.fea
├── instances
│   ├── AmstelvarA2-Roman_opsz8.ufo
│   ├── AmstelvarA2-Roman_opsz144.ufo
│   ├── AmstelvarA2-Roman_wdth85.ufo
│   ├── AmstelvarA2-Roman_wdth125.ufo
│   ├── AmstelvarA2-Roman_wght200.ufo
│   └── AmstelvarA2-Roman_wght800.ufo
├── AmstelvarA2-Roman.designspace
├── AmstelvarA2-Roman_avar1.designspace
└── AmstelvarA2-Roman_avar2.designspace
```

<dl>
<dt>*.ufo</dt>
<dd>Font sources in UFO format, with files named according to their variation parameters.<br/>
  All sources contain all glyphs, including glyphs which do not change in relation to the default (sources are not sparse).</dd>
<dt>measurements.json</dt>
<dd>Standalone JSON file containing definitions for various font- and glyph-level measurements.<br/>
  Created using the <a href='http://gferreira.github.io/fb-variable-values/reference/measurements/'>Measurements tool</a> from the VariableValues RoboFont extension.<br/>
  See <a href='http://gferreira.github.io/fb-variable-values/reference/measurements-format/'>Measurements format</a> for documentation of the data format.</dd>
<dt>blends.json</dt>
<dd>Standalone JSON file containing definitions of blended axes and blended sources from parametric axes.<br/>
  This data is used to build the avar2 designspace.</dd>
<dt>fences.json</dt>
<dd>Standalone JSON file containing definitions of min/max fence values for parametric values at blended sources.<br/>
  This data is used to add mappings for fences to the avar2 designspace. (experimental)</dd>
<dt>features</dt>
<dd>Subfolder with files containing OpenType code which can be linked to the source fonts.<br/>
  <em>Currently not used when building the variable fonts.</em></dd>
<dt>instances</dt>
<dd>Subfolder containing instances generated from the parametric sources, used to add blended axes to the avar1 designspace.<br/>
  Also useful for comparison with the original Amstelvar1 sources for blended extrema.</dd>
<dt>AmstelvarA2-Roman.designspace</dt>
<dd>Basic parametric designspace for use during design and development.<br/>
  Also used to build instances for the avar1 designspace.</dd>
<dt>AmstelvarA2-Roman_avar1.designspace</dt>
<dd>Designspace for building avar1 variable font.<br/>
  Includes the blended instances as sources for blended axes.</dd>
<dt>AmstelvarA2-Roman_avar2.designspace
<dd>Designspace for building avar2 variable font.<br/>
  Includes avar2 mappings which define blended sources from parametric values.</dd>
<!--
<dt>AmstelvarA2-Roman_avar2_fences.designspace
<dd>Experimental designspace containing avar2 mappings for fences.<br/>
  Includes avar2 mappings of fences for the default and blended extrema.</dd>
<dt>AmstelvarA2-Roman_avar2_fences-wght200.designspace
<dd>Experimental designspace containing avar2 fence mappings for one blended extreme only (wght200).<br/>
  Used while debugging avar2 implementation of fences.</dd>
-->
</dl>


Source/tools
-----

### Build script

The different designspaces and variable fonts are built by a single `build.py` script. The code is written around a core `AmstelvarDesignSpaceBuilder` object which provides common functionality to all AmstelvarA2 designspaces:

- reading all necessary data from the appropriate files and folders
- creating a designspace document with the parametric axes, taking min/max values from the UFO file names, and default values by measuring the default UFO
- adding the default source
- inserting parametric sources at their appropriate locations, based on actual measurements taken from each source
- adding blended axes using data from the `blends.json` file, and build blended sources as instances
- saving the designspace document into a `.designspace` file
- building a variable font for the current designspace

More specific designspaces inherit from this core object, and add their own special behavior around it.

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
  <!-- moved to Amstelvar1 repository: http://github.com/gferreira/amstelvar
  <dt>extract-measurements.py</dt>
  <dd>Extract measurements from one or more UFO sources into a dictionary. Optionally, save it into a JSON file.</dd>
  -->
  <dt>validate-locations.py</dt>
  <dd>Check if source locations are within the allowed min/max bounds for each axis.<br/>
    Helpful when debugging calculated blend values in relation to the current parametric axes.</dd>
</dl>

see also (on the RobotoFlex AVAR2 repository):

<dl>
  <dt><a href='http://github.com/googlefonts/roboto-flex-avar2/blob/main/Source/tools/mark-components.py'>mark-components.py</a></dt>
  <dd>Mark glyphs in the current font containing components with different colors depending on their components' nesting level.</dd>
</dl>


Blending
--------

The appropriate values for blending `opsz` `wght` `wdth` from parametric axes are produced on a [separate repository](http://github.com/gferreira/amstelvar) which is a fork of the original Amstelvar source. [The naming of UFO files was adjusted for easier parameter parsing (using underscores to separate parameters instead of hyphens), and all unnecessary files were deleted.]

A separate measurements file was added for Amstelvar, with the same parameters used for measuring AmstelvarA2. This file is needed because the contour structures of the two versions are different, and in most measurements different point indexes must be used.

### Designspace reduction

The intended designspace for AmstelvarA2 is smaller than the original Amstelvar designspace:

<table>
<tr>
<th></th>
<th colspan=2>Amstelvar</th>
<th colspan=2>AmstelvarA2</th>
</tr>
<tr>
<th>opsz</th>
<td>8</td>
<td>144</td>
<td>8</td>
<td>144</td>
</tr>
<tr>
<th>wght</th>
<td>100</td>
<td>1000</td>
<td>200</td>
<td>800</td>
</tr>
<tr>
<th>wdth</th>
<td>50</td>
<td>125</td>
<td>85</td>
<td>125</td>
</tr>
</table>

We create a basic Amstelvar designspace with `opsz` `wght` `wdth` axes, and use it to produce the corner locations of the AmstelvarA2 designspace as instances.

### Extracting measurements

These instances are then measured to produce the `blends.json` file which is used by the AmstelvarA2 designspace builder.
