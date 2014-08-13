# Dead simple owl class design patterns

## Motivation

We need a simple, lightweight standard for specifying design patterns
for generating documentation, generating new terms and for
retrofitting old ones.  The solution be readable and editable by anyone with a
basic knowledge of OWL and the ability to read manchester syntax.

Human readability requires that Manchester syntax be written using
labels, but sustainability and consistency checking requires.

## Approach

All owl object properties and classes are listed in a name -> ID
dictionary (hash lookup) attached to the class.

Variable interpolation into Manchester syntax and text is specified
using sprintf format.  Variable names are stored in associated lists.

For variables that are classes inserted into MS

## Validator

A validator will test:
* Integrity of the pattern
  * Are all owl entities in patterns in the dict?
  * Do all sprintf statements have an matching list of the correct length?
* Testing against a specified ontology

## 





