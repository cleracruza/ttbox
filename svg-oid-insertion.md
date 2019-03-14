# OID insertion in SVGs

This document describes how `ttbox`'s (semi-)automatic OID insertion
in SVGs works, how you can use it, and what to look out for.
If you want to see it in action right away, check out the
[ttbox-demo](https://github.com/cleracruza/ttbox-demo) project, which gives a
small but fully working example.

* [Motivation](#motivation)
* [Overview](#overview)
* [Usage](#usage)
* [Tips for SVG drawing](#tips-for-svg-drawing)
* [XSLT parameters](#xslt-parameters)



## Motivation

When building images for TipToi use, most
[tutorials](https://www.youtube.com/watch?v=QtdlwmKgg70) and
[examples](https://github.com/michote/Piraten-Geburtstag/tree/master/grafiken)
use pixel-based graphics programs (E.g.: [GIMP](https://www.gimp.org/)) to
prepare the OID-enriched graphics. That approach works fine and is straight
forward. But adding OIDs for so many objects is tedious, manual, repetitive
work. Especially, when shapes are beyond plain circles or rectangles. Even
worse: once manual OID placement is done, and one tries it out on a printout
with the TipToi pen, it more often than not occurs that one wants to move some
areas around a bit, one want to re-design certain aspects, or one wants to add
or remove a few objects. In all these cases, the manual OIDs placement needs to
be re-done. That wastes a lot of time.

When instead using vector-based graphic programs (E.g.:
[Inkscape](https://inkscape.org/)), moving objects is easy even after the
fact. And when using formats that allow for easy automatic manipulation (like
SVG), the manual OID placement part can be done mostly automatic. Hence, when
moving objects, or deleting objects, placed OIDs can be updated automatically.
This approach helps to shorten design cycles and overall saves a lot of time.

The OID-SVG insertion process implemented in `ttbox` is a very rough and
simplistic take on the problem that still leaves much to wish for, but drives
home the main benefits already.



## Overview

SVGs allow to add descriptions to elements. We use these descriptions to tag
elements with the name of the OID that should get overlaid.

The process goes like this:

1. Draw the plain SVG image without OIDs.
2. Select paths, rectangles, etc and add descriptions like for example `(oid:foo)` to mark elements that the OID `foo` should get added to the objects.
3. Use `tttool` (or the `project.mk` Makefile from `ttbox`) to generate OID png files from the project's YAML file.
4. Apply `svg-oid-insertion.xslt` to the plain image without OIDs. This step adds the needed OID patterns to the SVG, duplicates shapes, and finally applies the new OID patterns.
5. Print the generated`...-with-oids.svg` file and try it out.

Additionally, [start](#add-start-button) and [stop](#add-stop-button) buttons can get added automatically during the OID insertion.



## Usage

* To take advantage of `ttbox`'s OID insertion in SVGs, it's easiest to copy/clone/... the `ttbox` repo into your TipToi project as `ttbox`.

```
git clone https://github.com/cleracruza/ttbox.git
```

* Then, link `ttbox/Makefile.example` to `Makefile`:

```
ln -s ttbox/Makefile.example
```

* Run `make`
* Done.

See the [ttbox-demo](https://github.com/cleracruza/ttbox-demo) project, which
gives a small but fully working example.

If you're just interested in the bare-metal plain SVG manipulation, and do not
care about automatic OID png generation, OID tiling, etc, simply use an XSLT
processor (E.g.: [`xsltproc`](http://xmlsoft.org/XSLT/xsltproc.html)) to apply
the XSLT file `svg-oid-insertion.xsl` to your plain SVG. That's all that's
needed on the SVG side of things. Of course, you still need to generate the OID
pngs through some means as the SVG with OIDs relies on them.



## Tips for SVG drawing

### Adding `(oid:...)` tags to an object

To add tags like `(oid:...)` to an object, simply add them to the object's
`<desc>` child.

How to do that depends on the graphics program one uses, but in Inkscape select
the object, then go to the “Object” (German: “Objekt”) menu and select “Object
properties” (German: “Objekteigenschaften”), which should give you an “Object
properties" (German: “Objekteigenschaften”) form. To apply tags like `(oid:...)`
simply add them in that form's “Description” (German: “Beschreibung”) text area.

### Adding `(ttbox-...)` tags to the document

Some of `ttbox`'s tags (E.g.: [`(ttbox-start-button)`](#ttbox-start-button))
cannot be set on an object, but need to be set on the document itself, in the
metadata section.

How to do that depends on the graphics program one uses, but in Inkscape go to
the “File” (German: “Datei”) menu and select “Document Metadata” (German:
“Dokument-Metadaten”), which should give you a window showing “Dublin Core
Entities” form. To apply tags like `(ttbox-start-button)`, simply add them in
the “Description” (German: “Beschreibung”) field of the “Dublin Core Entities”
form.



### Crisp OIDs on printouts

For good OID recognition, it's paramount to get crisp pixels for OIDs patterns
on the printout. To achieve this, one needs to align the OID patterns to the
printer's pixels. Otherwise the OID patterns appear washed out and work poorly
or not at all.

Since SVG defaults to 90dpi pixels, and printers are 1200dpi (respectively
600dpi), aligning OID patterns at multiples of 3 (in SVGs pixels) is sufficient
(3 pixel at 90dpi are 40 pixel at 1200dpi (resp. 20 pixel at 600dpi)).

`ttbox` anchors patterns at `(0, 0)`, so the “multiples of 3” condition is met
per default. Yet there are a gotchas (like operations that might re-anchor
patterns), which we now show how to overcome.

Note that this “multiples of 3” is only relevant for the objects' patterns. The
objects themselves can of course be at any coordinates, say `(23.4,42.1)`,
without issues as long as their pattern keeps anchored at `(0,0)`.

#### Paper size

Some graphic programs (e.g.: Inkscape) choose the origin at the bottom-left
corner, while SVG has the origin in the top-left corner. This might give
counter-intuitive results with re-anchoring operations, like for example
aligning a group to Y-coordinate `9px`.

While in Inkscape's coordinate system `9px` looks clearly divisible by 3, in the
SVG coordinate system it becomes `9px from the paper's bottom edge`, which for
A4 paper boils down to `297mm - 9px`, which is `1043.36...px` and clearly not a
multiple of 3.

To avoid such issues due misalignment of SVG and graphics program coordinate
system, it's easiest to make the paper size a multiple of 3. So for example
instead of full A4 (210x297mm, which is `744.09x1052.36px`) pick `744x1050px`,
and each edge of the paper is suddenly a multiple of 3 in both SVG's and the
program's coordinate system.

And since your printer probably comes with print margins, pick a paper size that
accommodates for these margins to avoid scaling.

Paper sizes need not be multiples of 3, but it'll spare you head-aches later on
if they are.

#### Print settings

Programs typically allow to select paper sizes while ignoring printer margins
(E.g.: A4). When printing such documents, some programs/printer drivers allow
(or enforce) “Fit to page” (or “Scale to fit” or something similar). Avoid such
scalings/fittings as they ruin crispness of OID pattern pixels. Instead, choose
a slightly smaller paper size that accommodates for your printer's margins. For
example switching from a full A4 (210x297mm) to `672x909px` leaves 1cm margin on
both sides and 2cm margin on the top and bottom when printing on A4 paper.

#### Transformations on plain objects

In SVG, transformations of objects (moving, rotating, shearing, scaling, ...)
are typically stored in `transform` attributes. Use of this attribute, however,
affects the object's application of the OID pattern, and by re-anchoring
potentially distorts/mis-aligns the OID patterns. Hence, we want to avoid use of
`transform` wherever we can.

Some programs allow to automatically optimize away `transform`s whenever they
can. For example in Inkscape, go to the “File” menu, select “Inkscape
Preferences”, and in the popping up window, select “Transforms” in the tree view
on the left, and make sure “Store transformations” is set to “Optimized”.
This will make sure Inkscape pushes down transformations onto an object's
coordinates, if it can. For example with this setting at “Optimized” moving a
rect will not introduce a `transform` attribute, but will update the rect's `x`
and `y` attributes directly.

Some objects/transformations cannot be modeled directly without a `transform`
(E.g.: Scaling a circle, or rotating a rect). In such cases, converting the
objects to paths allows to avoid `transform`s. So for example to avoid a
`transform` when rotating a rect, first rotate the rect as desired. Then, having
the rotated rect selected, (in Inkscape) go to the “Path” menu, and select
“Object to Path”, and you'll get a path that's free of `transform` and hence
avoid the OID pattern re-anchoring.

Sometime graphics programs do not always optimize transformations on their
own. In such cases, moving the object a tiny bit, and moving it back, will (at
least in Inkscape) trigger optimization.

Some graphic programs (again Inkscape for example) do not push transformations
of groups down onto the individual objects. In such cases, align groups as
intended, and then ungroup (which pushes transformations down) and group again.

You can check whether or not `transform`s are used in the XML inspector of your
graphics program (E.g.: In Inkscape, go to the “Edit" menu and select “XML
Editor ...”).



## XSLT parameters

* [add-start-button](#add-start-button)
* [add-stop-button](#add-stop-button)
* [oidSize](#oidSize)
* [oidSuffix](#oidSuffix)
* [productId](#productId)
* [start-button-x](#start-button-x)
* [start-button-x-default](#start-button-x-default)
* [start-button-y](#start-button-y)
* [start-button-y-default](#start-button-y-default)
* [stop-button-x](#stop-button-x)
* [stop-button-x-default](#stop-button-x-default)
* [stop-button-y](#stop-button-y)
* [stop-button-y-default](#stop-button-y-default)



### add-start-button

Default: `true`, if the SVG's `subject` metadata contains `(ttbox-start-button)`. `false` otherwise.

If true, a start button is added to the generated SVG.



### add-stop-button

Default: `true`, if the SVG's `subject` metadata contains `(ttbox-stop-button)`. `false` otherwise.

If true, a stop button is added to the generated SVG.



### oidSize

Default: `30mm`

The size of the of the OID pngs in both X and Y coordinates.

This size is used to properly shape the patterns that fill the OID elements.



### oidSuffix

Default: None

A string that is inserted before the OID png file name's trailing `.png`.

If you cannot consume the pngs that tttool produces directly, but need to convert/scale/... them, you can use this setting to select the converted/scaled/... variant without overwriting the original. For example, if `tttool` generates a `oid-900-foo.png` for your project, you can store the converted/scaled/... variant as `oid-900-foo-scaled.png` and set the `oidSuffix` parameter to `-scaled` and then the `-scaled` will get picked up by this template.



### productId

Default: `900`

The product id.

The product id is needed to be able to include the OID pngs, as their name contains the product id.



### start-button-x

Default: `$VALUE`, if SVG's `subject` metadata contains `(ttbox-start-button-x:$VALUE)`, otherwise `start-button-x-default`

Start button offset from the page's left border.



### start-button-x-default

Default: 54

Start button's default offset from the page's left border.



### start-button-y

Default: `$VALUE`, if SVG's `subject` metadata contains `(ttbox-start-button-y:$VALUE)`, otherwise `start-button-y-default`

Start button offset from the page's bottom border.



### start-button-y-default

Default: -54

Start button's default offset from the page's bottom border.



### stop-button-x

Default: `$VALUE`, if SVG's `subject` metadata contains `(ttbox-stop-button-x:$VALUE)`, otherwise `stop-button-x-default`

Stop button offset from the page's right border.



### stop-button-x-default

Default: -54

Stop button's default offset from the page's right border.



### stop-button-y

Default: `$VALUE`, if SVG's `subject` metadata contains `(ttbox-stop-button-y:$VALUE)`, otherwise `stop-button-y-default`

Stop button offset from the page's bottom border.



### stop-button-y-default

Default: -54

Stop button's default offset from the page's bottom border.


