[![Build Status](https://travis-ci.org/INCATools/dead_simple_owl_design_patterns.svg?branch=master)](https://travis-ci.org/INCATools/dead_simple_owl_design_patterns)

# Dead simple owl design pattern (DOS-DP) exchange format

## For details please see:

[Dead Simple OWL Design Patterns](https://jbiomedsem.biomedcentral.com/articles/10.1186/s13326-017-0126-0)
David Osumi-Sutherland, Melanie Courtot, James P. Balhoff and Christopher Mungall
Journal of Biomedical Semantics 2017 8:18 DOI:10.1186/s13326-017-0126-0


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

See [full specification documentation](https://github.com/INCATools/dead_simple_owl_design_patterns/tree/master/src/schema/dosdp_schema.md)

## Setup

```
pip install dosdp
```

See https://pypi.org/project/dosdp/

## Validator spec

See [validator documentation](https://github.com/INCATools/dead_simple_owl_design_patterns/tree/master/src/dosdp/validator.md)

## Documentation generation spec

See [documentation_generation](https://github.com/INCATools/dead_simple_owl_design_patterns/tree/master/src/dosdp/document/document.md)

## Implementation

The aim of this project is to specify a simple design pattern system that can easily be consumed, whatever your code base.
This repository includes a simple Python validator (src/simple_pattern_tester.py).

For implementation, we recommend [dosdp-tools](https://github.com/INCATools/dosdp-tools).

## Uses

 * [ENVO](http://obofoundry.org/ontology/envo.html): envo [patterns/](https://github.com/EnvironmentOntology/envo/tree/master/src/envo/patterns)
 * [OBA](http://obofoundry.org/ontology/oba.html): oba [patterns/](https://github.com/obophenotype/bio-attribute-ontology/tree/master/src/ontology/patterns)
 * draft environmental conditions ontology: ecto [patterns/](https://github.com/cmungall/environmental-conditions/tree/master/src/patterns)
 * [Uberon](http://obofoundry.org/ontology/uberon.html): uberon [patterns/](https://github.com/obophenotype/uberon/tree/master/patterns)
 * [uPheno](https://github.com/obophenotype/upheno)
 * [Mondo](http://www.obofoundry.org/ontology/mondo.html)
