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
