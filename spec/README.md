### JSON-Schema spec for DOS-DP

The master schema files are in YAML. These are intended to be
converted to JSON for validation via JSON schema.


* DOSDP\_schema\_core.(yaml/json)  specifies the basic schema. It is
  intended to be sufficiently expressive for the specification of
  arbitrary OWL.  It includes a flexbile system for specifying
  variables ranging over OWL entites and data types. 
  
* DOSDP\_mapping\_schema.(yaml/json) specifies a mapping system for extending the
   core schema with derived fields.  Each derived field specifies a
   field type. 

* DOSDP\_convenience_fields.(yaml/json) specifies a set of derived
   fields for specifying logical axioms by type (EquivalentTo
   SubClassOf etc).   Patterns relying on these  fields are slightly
   less expressive than those using the full schema. For example, it
   is not possible to use the EquivalentTo field in cases where two
   equivalence axioms must be specified.   As this would break the
   unique key constraint of JSON.
   
* DOSDP\_OBO_fields.(yaml/json) specifies a set of derived fields OBO
   annotation property axioms.  This allows users familiar with OBO
   terminology to use familiar OBO tag names for annotation axioms.
   
    
  

