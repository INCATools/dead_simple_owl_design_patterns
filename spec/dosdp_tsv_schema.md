This spec follows: https://www.w3.org/TR/tabular-metadata/

However, a complete spec in JSON is not possible given that most columns will be derived from variable names.

Dialect Description is default apart from specifying tab as a separator. 
Doublequote may be used to escape whole cells but is not compulsory:

```json
{
  "encoding": "utf-8",
  "lineTerminators": ["\r\n", "\n"],
  "quoteChar": "\"",
  "doubleQuote": true,
  "skipRows": 0,
  "commentPrefix": "#",
  "header": true,
  "headerRowCount": 1,
  "delimiter": "\t",
  "skipColumns": 0,
  "skipBlankRows": false,
  "skipInitialSpace": false,
  "trim": false
}

```

Core spec

```json
{
  "url": "dosdp.tsv",
  "dc:title": "DOSDP TSV",
  "dcat:keyword": ["OWL", "design pattern"],
  "dc:publisher": {
    "schema:name": "DOSDP TSV",
    "schema:url": {"@id": "https://github.com/dosumis/dead_simple_owl_design_patterns/new/master/spec/"}
  }, 
  "dc:license": {"@id": "http://opendefinition.org/licenses/cc-by/"},
  "dc:modified": {"@value": "2017-06-21", "@type": "xsd:date"},
  "tableSchema": {
    "columns": [{
      "name": "defined_class",
      "dc:description": "A curie that expands to an IRI for the class being defined",
      "datatype": "string",
      "required": true
    }, {
      "name": "defined_class_label",
      "dc:description": "The label derived using the pattern spec. This should be left blank",
      "datatype": "string",
      "required": false
    }, {
      "name": "overide_label",
      "dc:description": "A column which allows the pattern derived label to be overriden with a user defined one.",
      "datatype": "string",
      "required": false

    }, {
      "name": "overide_definition",
      "dc:description": "A column which allows the pattern derived label to be overriden with a user defined one.",
      "datatype": "string",
      "required": false
    }],
    "primaryKey": "defined_class"
  }
}
```

Columns defined by pattern vars.  The name is derived from the variable name (indicated by {}).  `required : true` means that a column of this type must be present for each var/data_list_var specified in the pattern.


```json
 "columns": [{
      "name": "{var}",
      "dc:description": "A curie that expands to an IRI for var in the pattern spec.",
      "datatype": "string",
      "required": true
    }, {
      "name": "{var} label",
      "dc:description": "The label of the OWL enti",
      "datatype": "string",
      "required": false
    }, {
      "name": "{data_list_var}",
      "dc:description": "A pipe delimited list of literals, whose type is defined by the data_list_var in the pattern.",
      "datatype": "string",
      "delimiter": "|",
      "required": true
    }]
```
