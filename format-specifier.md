# Format.json format specifier

Format.json is a JSON-compliant file which details which attributes should be put 
in the output and how.

It consists of an array of objects, where each object specifies one attribute.

Each attribute object is as follows:`
{
    "name" : <string>,
    "type" : <type-specifier>,
    <type-specific-arguments>,
    "source" : <string>,
    "subsource" : <string>
}`

A `<type-specifier>` is one of:

 - "string"

 - "stringConcat"

 - "numeric"

 - "boolean"

 - "nominal"

 - "alias"

 - "extracted"

 - "datetime"

Attributes are processed differently per-specifier. Details of these proceed later 
in the document.

The `name` of an attribute is passed on to the output. Additionally, for all type 
specifiers except `alias`, it is the name used in the source file for the object 
at the lowest level.

The `source` of an attribute is either "channel" or "video". It is prepended to 
the attribute name in the output, as "`source` - `name`". If it is "channel", the 
subsource in the top-level of a source-file object will be used. If it is 
"videos", the attribute will be collected over each object in the "videos" array 
in the source-file, and merged into a single value (dependent on the type specifier).

The `subsource` of an attribute is the name of the object, in the source-file 
object being searched, where the attribute data is found.

The attribute is therefore located as follows for non-`alias` types. Assume that 
the source-file has been loaded into an object `data`, that `i` is an index 
specifying a valid offset within the top-level array of `data`, and that for 
videos `j` is an index specifying a valid offset within the array of videos. 
Attribute data is found by `data[i][subsource][name]` for `source=="channel"`, and 
by `data[i][videos][j][subsource][name]` for `source=="video"`.

## `alias`

Attributes of type `alias` are special in that they do not use the `source` or 
`subsource` attributes. An attribute of type `alias` takes on the value of a 
target attribute, which is not itself written into the output, with the new name 
specified by `name`. An attribute of type `alias` is specified by three 
parameters: The always-required `name` and `type`, and the type-specific-argument 
`target`, where `target` is an attribute object of any type besides `alias`.

Note that because `alias` does not use the `source` argument, the `name` given 
will be written to the output file as-is. `alias` attributes which need to include 
the video/channel tag therefore need to have it in their `name`.

## `extracted`

Attributes of type `extracted` are those which are processed (more than 
`stringConcat`) before being written into the output. In particular, they are 
those where the desired data isn't exactly what is written in the source-file. Two 
examples of this are data within strings: "THIS IS A VALUE: 'abc' THAT WAS A 
VALUE", or when the desired output is some metadata of the source-file attribute 
(for example, the length of the string).

An attibute of type `extracted` has the type-specific-argument `extraction`.

`extraction` is an object in the following format:`
{
    "goal" : <type-specifier>,
    "source" : <source-specifier>,
    "specifier" : <optional string>
}`

`goal` is any type-specifier besides `alias`. If `goal` is "extracted", then 
another `extraction` object must be provided in the current one: this object may 
**not** have the same `source` as *any* `extraction` object it is contained in (no 
current `<source-specifier>` is complex enough that this would be of use anyway - 
If this changes, this requirement will be revisited). The type specifier of `goal` 
will replace the type specifier of the attibute once extraction is complete. If it 
is `extracted`, then this process will be repeated (more deeply-nested extractions 
will be performed later). Otherwise, the attibute will continue processing as the 
specified type.

A `<source-specifier>` is one of the following:

 - "stringLength"
 
 - "regex"
 
If the source specifier is "stringLength", then `goal` must be `numeric`, and the 
attibute data in the source-file must be a string. The result will simply be the 
length (number of characters in) the string.

If the source specifier is "regex", then the attibute data in the source-file must 
be a string, and the `specifier` parameter of the `extraction` object must be a 
regular expression to run on the data in the source-file. The result of this 
operation will be the result of the extraction, casted to the goal datatype.
