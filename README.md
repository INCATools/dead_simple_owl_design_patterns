[![Build Status](https://travis-ci.org/dosumis/dead_simple_owl_design_patterns.svg?branch=master)](https://travis-ci.org/dosumis/dead_simple_owl_design_patterns)

# Dead simple owl design pattern (DOS-DP) exchange format

## Motivation

The job of editing the GO and many other OBOish OWL ontologies increasingly involves specifying OWL design patterns.  We need a simple, light-weight standard for specifying these design patterns that can then be used for generating documentation, generating new terms and retrofitting old ones. The solution must be readable and editable by anyone with a basic knowledge of OWL and the ability to read manchester syntax.  It must also be easy to use programatically without the need for custom parsers - i.e. it should follow some existing data exchange standard.

Human readability and editability requires that Manchester syntax be written using labels, but sustainability and consistency checking requires that the pattern record IDs. 

## Approach

* Patterns are specified in the subset of YAML that can be converted to JSON.
  * JSON format is the ideal exchange format for programatic consumption: It is already javascript; Standard libraries are available to convert it into datastructures in many languages;Developers are typically experienced at consuming it. 
  * *But* YAML is much easier than JSON for humans to edit (it can be difficult for human editors to keep curly braces and quotes balanced and to add commas correctly in JSON). YAML also has the great advantage over JSON of allowing comments to be embedded. [Conversion between YAML and JSON is trivial](http://yamltojson.com/)

* All patterns contain dictionaries (hash lookups) that can be used to lookup up OWL shortform IDs from labels.  OWL ShortFormIDs are assumed to be sufficient for entity resolution during usage of the pattern.  Labels are assumed to be sufficient for entity resolution _within_ a pattern.

* Variable interpolation into Manchester syntax and text is specified using [printf format strings](https://en.wikipedia.org/wiki/Printf_format_string).  Variable names are stored in associated lists.

* Variables are specified in a dictionary with variable name as key and value as range specified as a Manchester syntax expresssion.

## Specification:

[Full specification using JSON-schema](https://github.com/dosumis/dead_simple_owl_design_patterns/tree/master/spec/README.md).

The following is a quick guide to commonly used fields, with an emphasis on OBO-specific (derived) fields:

Manchester syntax expressions use names (labels).  These are always single quoted inside an expression that is double quoted. (Note single quotes in term names must be escaped).

* __pattern\_name__ (string): the name of the pattern. No spaces or special characters allowed.
* __description__(string): Text describing the pattern and its uses.  For use in documentation - not in OWL files.
* __classes__ (associative array): hash lookup for OWL classes used in the pattern. key = name, value = ID
* __relations__ (associative array): hash lookup for OWL object properties (relations) used in the pattern. key = name, value = ID
* __vars__ (associative array): a hash lookup for vars in the pattern, key = var name, value = range expressed as manchester syntax.
* __name__  (associative array): 
  * __text__ (string): sprintf label text
  * __vars__ (string): list of vars for interpolation of class names into sprintf of text.
* __def__ (associative array): 
  * __text__ (string): sprintf definition text.  
  * __vars__ (array): List of vars for interpolation of class names into sprintf of text. 
* __comment__(string)
* __EquivalentTo__ (associative array): 
  * __text__ (string): Sprintf OWL Manchester syntax string.  All OWL entities must be quoted; %s not quoted).
  * __vars__ (array): List of vars for interpolation into sprintf owl MS text.


Draft yaml example - [import_into_cell](patterns/import_into_cell.yaml)

Draft json example - [import_into_cell](patterns/import_into_cell.json)


## Validator spec

### Basic validation

1. test converstion of YAML to JSON
2. validate against JSON schema (e.g. see [test_schema.py](https://github.com/dosumis/dead_simple_owl_design_patterns/blob/master/spec/test_schema.py))


### Recommendations for additional validation outside of JSON schema:

* For all printf fields, 
  * test length of var array matches number of interpolation slots in string
  * test that all var names are valid for the pattern
* For printf_owl fields:
   * Check quoted names in the printf field correspond to dictionary entries in the pattern.
  
* Tests against referenced ontologies:
   * Are the entities in the dictionaries present and non-obsolete in the latest releases of the relevant ontologies?
   * Are the readable names up to date ?
   * For all printf manchester syntax strings: Is a valid Manchester syntax string generated when variable slots are filled using the range for each variable?
   
* Validation when creating instances:
   * Are values for variable slots present and non-obsolete in the latest releases of the relevant ontologies?
   * Are values for the variable slots in the specified range?


## Implementation

The aim of this project is to specify a simple design pattern system that can easily be consumed, whatever your code base.
This repository includes a simple Python validator (src/simple_pattern_tester.py).

For implementation, we recommend [dosdp-tools](https://github.com/balhoff/dosdp-tools).


## Uses

 * [ENVO](http://obofoundry.org/ontology/envo.html): envo [patterns/](https://github.com/EnvironmentOntology/envo/tree/master/src/envo/patterns)
 * [OBA](http://obofoundry.org/ontology/oba.html): oba [patterns/](https://github.com/obophenotype/bio-attribute-ontology/tree/master/src/ontology/patterns)
 * draft environmental conditions ontology: ecto [patterns/](https://github.com/cmungall/environmental-conditions/tree/master/src/patterns)
 * [Uberon](http://obofoundry.org/ontology/uberon.html): uberon [patterns/](https://github.com/obophenotype/uberon/tree/master/patterns)
