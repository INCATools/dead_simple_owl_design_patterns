# Dead simple owl design pattern exchange format

## Motivation

The job of editing the GO and many other OBOish OWL ontologies increasingly involves coming up with new design patterns.  We need a simple, lightweight standard for specifying these design patterns that can then be used 
for generating documentation, generating new terms
retrofitting old ones. The solution must be readable and editable by anyone with a
basic knowledge of OWL and the ability to read manchester syntax.  It must also be easy
to use programatically without the need for custom parsers - i.e. it should follow some 
existing data exchange standard.

Human readability and editability requires that Manchester syntax be written using
labels, but sustainability and consistency checking requires that 
the pattern record IDs. 


## Approach

* JSON format is probably the ideal exchange format for programatic consumption. It is already javascript.  Standard libraries are available to convert it into datastructures in many languages. Developers are typically experience at consuming it. But it can be difficult for human editors to keep curly braces and quotes balanced and to add commas correctly.  The subset of YAML that can be converted to JSON is much easier for humans to keep well-formed, so this will be the master format.  YAML also has the great advantage over JSON of allowing comments to be embedded.

* All owl object properties and classes are listed in a name -> ID dictionary (hash lookup) attached to the class.

* Variable interpolation into Manchester syntax and text is specified using sprintf format.  Variable names are stored in associated lists.

* Varibles are specified in a dictionary with variable name as key and value as range specified as a Manchester syntax expresssion.

## Draft spec:

Manchester syntax expression use names (labels).  These are always single quoted.

* __pattern\_name__ (string): the name of the pattern. No spaces or special characters allowed.
* __owl\_entities__ (associative array): hash lookup for OWL entities used in the pattern, key = name, value = ID
* __vars__ (associative array): a hash lookup for vars in the pattern, key = var name, value = range expressed as manchester syntax.
* __def__ (associative array): 
  * __text__ (string): sprintf definition text.  
  * __vars__ (array): List of vars for interpolation of class names into sprintf of text. 
* __EquivalentTo__ (associative array): 
  * __owl__ (string): Sprintf OWL Manchester syntax string.
  * __vars__ (array): List of vars for interpolation into sprintf owl MS text.

### yaml
```.yaml

pattern_name : some_name_with_no_spaces_or_special_chars
owl_entities :  
  class1 : ID1 
  objectProperty1 : ID2 
  class2 : ID3 
    
vars :  
  var1 : 'class2' 
    
def: 
  text: Ipsum lorum %s dolor sit amet, consectetur adipiscing elit. Fusce gravida non erat et gravida.
  vars:
    - var1
    
EquivalentTo: 
  owl: 'objectProperty1' some 'class1'
  vars:
    - var1
```

### json

```.javascript

   { 
    "pattern_name" : "some_name_no_spaces_of_special_chars",
    "owl_entities" : { 
	"class1" : "ID1", 
	"objectProperty1" : "ID2", 
	"class2" : "ID3", 
    },
    "vars" : { 
	"var1" : "'class2'" 
    },
    "def": {
	"text": "Ipsum lorum %s dolor sit amet, consectetur adipiscing elit. Fusce gravida non erat et gravida.", // 
	"vars": ["var1"]
    },
    "EquivalentTo": {
	"owl": "'objectProperty1' some 'class1'",
	"vars": ["var1"]
    }
   }
```

See [draft json example](json/draft_json_example.json)

See [draft yaml example](yaml/)


## Validator spec

(Basic JSON validation can be done using standard libraries)

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






