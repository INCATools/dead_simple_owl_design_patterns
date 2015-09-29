## Installation

Requires [Jython 2.7](http://www.jython.org/downloads.html) and [Brain](https://github.com/loopasam/Brain/wiki#local).

Both are available via Maven.

## pattern.py

Pattern processing: 

- pattern.abstract_pattern(pattern, ont) - initialisation validates pattern doc
- pattern.applied_pattern(pattern, cdict, ont) - intitialisation validates pattern doc + var spec. 

   - ont = 'a Brain object'
   - pattern = 'pattern document as python data structure' (e.g. loaded from JSON or YAML file)
   - cdict = specification of vars as dict of 2 element lists or tuples:
        { var1 : ( name , id ), var2: ( ... }

Basic methods:

 - pattern.abstract_pattern.gen_markdown_doc()
 - pattern.applied_pattern.add_class_to_ont(ID)
   - ID = OWL shortFormID. ID generation should be done separately. BaseURI should be set during construction of Brain object. 
 - pattern.applid_pattern.gen_markdown_doc()



## Runners

- yaml2json_runner.py - convert all ../paterns/*.yaml to json (may be run as Python)
- abstract_pattern_runner.py  - validate all patterns(json), and generate markdown doc for patterns (must be run as Jython)
