Checklist for AmstelvarA2 ASCII release
=======================================

TO-DO
-----

- [ ] match reference fonts to parametric default (ASCII)
- [ ] fix bug in automatic GDEF table
- [ ] fix width of figures in Roman opsz8
- [ ] kerning
- [ ] update README
- [ ] implement `rvrn` feature for /Q /dollar
- [ ] STAT table [(issue #205)](https://github.com/googlefonts/amstelvar-avar2/issues/205)

### Done!

- [x] add parent parametric axes (correctly)
- [x] tuning of composite glyphs
- [x] fix bug with blended axes in Chrome [(issue #215)](https://github.com/googlefonts/amstelvar-avar2/issues/215)
- [x] split etcetera from lowercase
- [x] add instances (pre-defined styles)
- [x] move Amstelvar reference files to AmstelvarA2 repository

Deliverables
------------

- [x] avar2 variable font Roman & Italic (ASCII subset)
  - [x] no tuning
  - [x] full tuning (duovars + trivars + quadvars)
- [ ] README with updated project info
- [ ] static instances?

<!--
- [ ] avar1 designspace + variable font [(issue #204)](https://github.com/googlefonts/amstelvar-avar2/issues/204)
  - [ ] only user axes (weight, width, optical size, grade)
  - [ ] only user + primary parametric axes (weight, width, optical size, grade + xopq, yopq, xtra, xtsp, ytlc)
  - [ ] all axes, same as the avar2 build
-->
