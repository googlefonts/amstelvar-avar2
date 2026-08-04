Different implementations of the AmstelvarA2 designspace
========================================================


Common to both approaches
-------------------------

Parametric mappings (blends) for 26 corner locations:

```xml
<mappings>
  <mapping description="opsz144">
    <input>
      <dimension name="Optical size" xvalue="144"/>
    </input>
    <output>
      <dimension name="XOUC" xvalue="84"/>
      <dimension name="XOLC" xvalue="78"/>
      <dimension name="XOFI" xvalue="80"/>
      <dimension name="XTUC" xvalue="348"/>
      <dimension name="XTUR" xvalue="470" />
      <dimension name="XTUD" xvalue="410" />
      ...
    </output>
  </mapping>
  ...
</mappings>
```


1\. Tuning axes and tuning sources
----------------------------------

### Axes

Tuning is implemented by adding 26 new parametric axes (`TN00`-`TN25`) to the designspace:

```xml
<axes>
  ...
  <axis tag="TN00" name="TN00" minimum="0" maximum="100" default="0" hidden="1"/> <!-- opsz144 -->
  <axis tag="TN01" name="TN01" minimum="0" maximum="100" default="0" hidden="1"/> <!-- opsz144 wdth125 -->
  <axis tag="TN02" name="TN02" minimum="0" maximum="100" default="0" hidden="1"/> <!-- opsz144 wdth50 -->
  <axis tag="TN03" name="TN03" minimum="0" maximum="100" default="0" hidden="1"/> <!-- opsz144 wght100 -->
  ...
</axes>
```

### Sources

Tuning sources are inserted in the parametric designspace, with each tuning axis controlling one tuning source:

```xml
<source filename="tuning/opsz144.ufo" name="opsz144" familyname="AmstelvarA2 Roman" stylename="opsz144">
  <location>
    default parameters +
    <dimension name="TN00" xvalue="100"/>
    <dimension name="TN01" xvalue="0"/>
    <dimension name="TN02" xvalue="0"/>
    <dimension name="TN03" xvalue="0"/>
    ...
  </location>
</source>
```

### Example

- [AmstelvarA2 Roman designspace with tuning sources](https://github.com/gferreira/amstelvar-avar2/blob/main/Sources/Roman/AmstelvarA2-Roman.designspace)



2\. Reference sources
---------------------

### Axes

No additional axes required.

### Sources

Reference sources are inserted in the parametric designspace, using the same parametric locations as the blend mappings:

```xml
<source filename="reference/Amstelvar-Roman_opsz144.ufo" name="opsz144" familyname="AmstelvarA2" stylename="opsz144">
  <location>
    <dimension name="WDSP" xvalue="267"/>
    <dimension name="XOUC" xvalue="84"/>
    <dimension name="YOUC" xvalue="16"/>
    <dimension name="XOUA" xvalue="60"/>
    <dimension name="YOUA" xvalue="20"/>
    ...
  </location>
</source>
```

### Example

- [AmstelvarA2 Roman designspace with reference sources](https://github.com/gferreira/amstelvar-avar2/blob/main/Sources/Roman/AmstelvarA2-Roman_v2.designspace)

