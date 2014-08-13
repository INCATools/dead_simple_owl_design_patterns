# Dead simple owl design pattern exchange format

## Motivation

We need a simple, lightweight standard for specifying design patterns
for generating documentation, generating new terms and for
retrofitting old ones. The solution must be readable and editable by anyone with a
basic knowledge of OWL and the ability to read manchester syntax.  It must also be easy
to use programatically without the need for custom parsers - i.e. it should follow some 
existing data exchange standard.

Human readability and editability requires that Manchester syntax be written using
labels, but sustainability and consistency checking requires that 
the pattern record IDs. 


## Approach

* Use JSON format:  If kept simple, it is easy to read and edit. It is easy to work with programatically - standard libraries are available to convertit into datastructures in many languages.

* All owl object properties and classes are listed in a name -> ID dictionary (hash lookup) attached to the class.

* Variable interpolation into Manchester syntax and text is specified using sprintf format.  Variable names are stored in associated lists.

* Varibles are specified in a dictionary with variable name as key and value as range specified as a Manchester syntax expresssion.

## Draft spec:

See []() for example.


## Validator spec

A validator will test:
* Integrity of the pattern
  * Are all owl entities in patterns in the dict?
  * Do all sprintf statements have an matching list of the correct length?
* Testing against a specified ontology:
  * Are the entities in the dictionary non-obsolete?
  * Are the names up to date ?






