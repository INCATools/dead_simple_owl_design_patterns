# DOSDP

- [Properties](#properties)
  * [OWL Entity Dictionaries](#owl-entity-dictionaries)
  * [Var Types](#var-types)
  * [Var Munging](#var-munging)
  * [Axioms](#axioms)
  * [Logical Convenience Fields](#logical-convenience-fields)
  * [OBO fields](#obo-fields)
  * [Instance Graph Spec](#instance-graph-spec)

## Properties

- **`pattern_name`** *(string)*: The name of the pattern.  This must be an ASCII string with no spaces. The only special characters allowed are '_' and '-'. By convention, this is used as the file name of the pattern - with an appropriate extension.


- **`pattern_iri`** *(string)*: A global identifier for the pattern. This can be a full IRI or a CURIE, using the same prefix mappings as other CURIEs in the pattern.


- **`base_IRI`** *(string)*: Specifies the base IRI to be used to generate new classes.


- **`contributors`** *(array)*: A list of authors of a pattern. Each author must be specified using a URL or Curie - we recommend ORCID. We do not recommend that this list is instantiated in terms generated using a pattern, but where it is it should be instantiated as a set of annotation axioms using dc:contributor.
  - **Items** *(string)*


- **`description`** *(string)*: A free text description of the pattern.  Must be UTF-8 encoded.


- **`examples`** *(list)*: A list of example terms implementing this pattern.
  - **Items** *(string)*


- **`status`** *(string)*: Implementation status of pattern. Must be one of: `['development', 'published']`.


- **`tags`** *(list)*: A list of strings used to tag a pattern for the purposes of arbitrary, cross-cutting grouping of patterns.
  - **Items** *(string)*


- **`readable_identifiers`** *(array)*: A list of annotation properties used as naming fields, in order of preference.
  - **Items** *(string)*


### OWL Entity Dictionaries



- **`classes`** *(object)*: A dictionary of OWL classes. key :label; value : short form id.


- **`objectProperties`** *(object)*: A dictionary of OWL object properties. key : label; value : short form id.


- **`relations`** *(object)*: A dictionary of OWL object properties. key : label; value : short form id.


- **`dataProperties`** *(object)*: A dictionary of OWL data properties key : label; value : short form id.


- **`annotationProperties`** *(object)*: A dictionary of OWL annotation properties key : label; value : short form id.


### Var Types



- **`vars`** *(object)*: A dictionary of variables ranging over OWL classes. Key = variable name, value = variable range as manchester syntax string.


- **`list_vars`** *(object)*: A dictionary of variables refering to lists of owl classes. Key = variable name, value = variable range of items in list specified as a valid OWL data-type.


- **`data_vars`** *(object)*: A dictionary of variables ranging over OWL data-types. Key = variable name, value = variable range specified as a valid OWL data-type.


- **`data_list_vars`** *(object)*: A dictionary of variables rrefering to lists of some specified OWL data-types. Key = variable name, value = variable range of all items in list, specified as a valid OWL data-type.


### Var Munging



- **`substitutions`** *(array)*
  - **Items**: Refer to *#/definitions/regex_sub*.
> - **`regex_sub`** *(object)*: Cannot contain additional properties.
>   - **`in`** *(string)*: name of input var.
>   - **`out`** *(string)*: Name of output var.  If input var specified an OWL entity then readable identifier is used as input to substitution.
>   - **`match`** *(string)*: perl style regex match.
>   - **`sub`** *(string)*: perl style regex sub.  May include backreferences.


### Axioms



- **`annotations`** *(array)*
  - **Items**: Refer to *#/definitions/annotations*.
> - **`annotations`** *(array)*: One of the followings:
>   - **Items**: Refer to *#/definitions/printf_annotation*.
>>- **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>  - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>  - **`annotations`** *(array)*
>>    - **Items**: Refer to *#/definitions/annotations*.
>>   - **`text`** *(string)*: A print format string.
>>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>     - **Items** *(string)*
>   - **Items**: Refer to *#/definitions/list_annotation*.
>>- **`list_annotation`** *(object)*: Cannot contain additional properties.
>>  - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>  - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>  - **Items**: Refer to *#/definitions/iri_value_annotation*.
>> - **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>   - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>   - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>   - **`annotations`** *(array)*
>>     - **Items**: Refer to *#/definitions/annotations*.


- **`logical_axioms`** *(array)*
  - **Items**: Refer to *#/definitions/printf_owl*.
> - **`printf_owl`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`axiom_type`** *(string)*: OWL axiom type expressed as manchester syntax: equivalentTo, subClassOf, disjointWith. GCI  - for general class inclusion axioms, is also valid (although missing from manchester syntax.) This specifies the axiom type to be generated from the text following substitution.'. Must be one of: `['equivalentTo', 'subClassOf', 'disjointWith', 'GCI']`.
>   - **`text`** *(string)*: A print format string in OWL Manchester syntax. Each entry must correspond to an entry in o the name of a var in the var field of the pattern. Entries in single quotes must correspond to the labels of entries in owl_entity dictionaries (classes, relations, dataProperties).
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. An empty var list can be specified simply by leaving this field out.
>     - **Items** *(string)*


- **`name`**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


- **`comment`**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


- **`def`**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


- **`namespace`**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


### Logical Convenience Fields

Where only one of any OWL axiom type is present, these convenience fields may be used.

- **`equivalentTo`**: Refer to *#/definitions/printf_owl_convenience*.
> - **`printf_owl_convenience`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`text`** *(string)*: A print format string in OWL Manchester syntax. Each entry must correspond to an entry in o the name of a var in the var field of the pattern. Entries in single quotes must correspond to the labels of entries in owl_entity dictionaries (classes, relations, dataProperties).
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern.
>     - **Items** *(string)*


- **`subClassOf`**: Refer to *#/definitions/printf_owl_convenience*.
> - **`printf_owl_convenience`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`text`** *(string)*: A print format string in OWL Manchester syntax. Each entry must correspond to an entry in o the name of a var in the var field of the pattern. Entries in single quotes must correspond to the labels of entries in owl_entity dictionaries (classes, relations, dataProperties).
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern.
>     - **Items** *(string)*


- **`GCI`**: Refer to *#/definitions/printf_owl_convenience*.
> - **`printf_owl_convenience`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`text`** *(string)*: A print format string in OWL Manchester syntax. Each entry must correspond to an entry in o the name of a var in the var field of the pattern. Entries in single quotes must correspond to the labels of entries in owl_entity dictionaries (classes, relations, dataProperties).
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern.
>     - **Items** *(string)*


- **`disjointWith`**: Refer to *#/definitions/printf_owl_convenience*.
> - **`printf_owl_convenience`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`text`** *(string)*: A print format string in OWL Manchester syntax. Each entry must correspond to an entry in o the name of a var in the var field of the pattern. Entries in single quotes must correspond to the labels of entries in owl_entity dictionaries (classes, relations, dataProperties).
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern.
>     - **Items** *(string)*


### OBO fields



- **`exact_synonym`**: Refer to *#/definitions/list_annotation_obo*.
> - **`list_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references. Use of this field should add the same xref set to all annotation axioms generated.


- **`narrow_synonym`**: Refer to *#/definitions/list_annotation_obo*.
> - **`list_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references. Use of this field should add the same xref set to all annotation axioms generated.


- **`related_synonym`**: Refer to *#/definitions/list_annotation_obo*.
> - **`list_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references. Use of this field should add the same xref set to all annotation axioms generated.


- **`broad_synonym`**: Refer to *#/definitions/list_annotation_obo*.
> - **`list_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references. Use of this field should add the same xref set to all annotation axioms generated.


- **`xref`**: Refer to *#/definitions/list_annotation_obo*.
> - **`list_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references. Use of this field should add the same xref set to all annotation axioms generated.


- **`generated_synonyms`** *(array)*: An OBO convenience field to allow the specification of exact synonyms generated by interpolation of OWL entity names into printf text. Each entry may be annotated.
  - **Items**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


- **`generated_narrow_synonyms`** *(array)*: An OBO convenience field to allow the specification of narrow synonyms generated by interpolation of OWL entity names into printf text. Each entry may be annotated.
  - **Items**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


- **`generated_broad_synonyms`** *(array)*: An OBO convenience field to allow the specification of broad synonyms generated by interpolation of OWL entity names into printf text. Each entry may be annotated.
  - **Items**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


- **`generated_related_synonyms`** *(array)*: An OBO convenience field to allow the specification of related synonyms generated by interpolation of OWL entity names into printf text. Each entry may be annotated.
  - **Items**: Refer to *#/definitions/printf_annotation_obo*.
> - **`printf_annotation_obo`** *(object)*: Cannot contain additional properties.
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`xrefs`** *(string)*: Takes the name of a single data_list_var specifying a list of database cross references.
>   - **`text`** *(string)*: A print format string.
>   - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.
>     - **Items** *(string)*


### Instance Graph Spec



- **`instance_graph`** *(object)*: Cannot contain additional properties.
  - **`nodes`** *(object)*: Key = name of individual within this pattern doc Value = Type of individual specified using either the quoted name of a class in the class dictionary of this pattern or a var name.  This field does not support typing via anonymous class expressions.
  - **`edges`** *(array)*
    - **Items**: Refer to *#/definitions/opa*.
> - **`opa`** *(object)*: Cannot contain additional properties.
>   - **`edge`** *(array)*: A triple specified as an ordered array with 3 elements [subject, rel, object] * rel must be the quoted name of a relation from the relations (object property) dictionary. * subject and object must be the name of an individual specified in the nodes field.
>     - **Items** *(string)*
>   - **`annotations`** *(array)*
>     - **Items**: Refer to *#/definitions/annotations*.
>>- **`annotations`** *(array)*: One of the followings:
>>  - **Items**: Refer to *#/definitions/printf_annotation*.
>>> - **`printf_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`annotations`** *(array)*
>>>     - **Items**: Refer to *#/definitions/annotations*.
>>>  - **`text`** *(string)*: A print format string.
>>>  - **`vars`** *(array)*: An ordered list of variables for substitution into the accompanying print format string. Each entry must correspond to the name of a variable specified in either the 'vars' field or the data_var field of the pattern. Where an OWL entity is specified, the label for the OWL entity should be used in the substitution.  An empty var list can be specified simply by leaving this field out.
>>>    - **Items** *(string)*
>>  - **Items**: Refer to *#/definitions/list_annotation*.
>>> - **`list_annotation`** *(object)*: Cannot contain additional properties.
>>>   - **`annotationProperty`** *(string)*: A string corresponding to the rdfs:label of an owl annotation property. If the annotation property has no label, the shortForm ID should be used. The annotation property must be listed in the annotation property dictionary.'.
>>>   - **`value`** *(string)*: A single list variable (list_var or data_list_var).  Each item in this list should be used to generate a separate annotation axiom.
>>   - **Items**: Refer to *#/definitions/iri_value_annotation*.
>>>- **`iri_value_annotation`** *(object)*: Cannot contain additional properties.
>>>  - **`annotationProperty`** *(string)*: A string corresponding to a key in the annotation property dictionary.
>>>  - **`var`** *(string)*: The name of a variable specified in the 'vars' field. The IRI of the variable value will be the object of the annotation axiom.
>>>  - **`annotations`** *(array)*
>>>    - **Items**: Refer to *#/definitions/annotations*.
>   - **`not`** *(boolean)*: Optional field for negated OPAs.


