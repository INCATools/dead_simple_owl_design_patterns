# Dead simple owl design pattern (DOS-DP) exchange format

## Motivation

The job of editing the GO and many other OBOish OWL ontologies increasingly involves specifying OWL design patterns.  We need a simple, light-weight standard for specifying these design patterns that can then be used for generating documentation, generating new terms and retrofitting old ones. The solution must be readable and editable by anyone with a basic knowledge of OWL and the ability to read manchester syntax.  It must also be easy to use programatically without the need for custom parsers - i.e. it should follow some existing data exchange standard.

Human readability and editability requires that Manchester syntax be written using labels, but sustainability and consistency checking requires that the pattern record IDs. 

## Approach

* Patterns are specified in the subset of YAML that can be converted to JSON.
  * JSON format is the ideal exchange format for programatic consumption: It is already javascript; Standard libraries are available to convert it into datastructures in many languages;Developers are typically experienced at consuming it. 
  * *But* YAML is much easier than JSON for humans to edit (it can be difficult for human editors to keep curly braces and quotes balanced and to add commas correctly in JSON). YAML also has the great advantage over JSON of allowing comments to be embedded. [Conversion between YAML and JSON is trivial](http://yamltojson.com/)

* All pattern contain dictionaries (hash lookups) that can be used to lookup up OWL shortform IDs from labels.  OWL ShortFormIDs are assumed to be sufficient for entity resolution during usage of the pattern.  Labels are assumed to be sufficient for entity resolution _within_ a pattern.

* Variable interpolation into Manchester syntax and text is specified using sprintf format.  Variable names are stored in associated lists.

* Variables are specified in a dictionary with variable name as key and value as range specified as a Manchester syntax expresssion.

## Draft spec:

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

(Basic JSON/YAML validation can be done using standard libraries)

A validator will test:
* Integrity of the pattern
  * Are all keys valid?
  * Are all values of the correct type?
  * Are a minimal set of keys present?
  * Are all owl entities in patterns in the dict?
  * Do all sprintf statements have an matching list of the correct length?
* Testing against a specified ontology:
  * Are the entities in the dictionary non-obsolete?
  * Are the names up to date ?

## Implementation

The aim of this project is to specify a simple design pattern system that can easily be consumed, whatever your code base.  This repository includes [code for validation, documentation and generation of pattern-based classes](https://github.com/dosumis/dead_simple_owl_design_patterns/tree/master/src) written in Jython.





