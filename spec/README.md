### JSON-Schema spec for DOS-DP


* DOSDP\_schema\_core.yaml  specifies the basic schema. It is
  intended to be sufficiently expressive for the specification of
  arbitrary OWL.  It includes a flexbile system for specifying
  variables ranging over OWL entites and data types.  It also includes
  convenience fields for use in patterns that don't have multiple logical
  axioms of the same type.
 
   
* DOSDP\_OBO_fields.(yaml/json) extends (via import) the core schema, specifyng a 
   set of a set of convenience fields that map to standard OBO annotation
   property types.  The mapping is included in the schema files in a field that 
   is not part of JSON-schema. Fields are named for OBO tags. This allows users familiar with OBO
   terminology to use familiar OBO tag names for annotation
   axioms. 
   
Validation runs via Travis using test_schema.py
   
    
  

