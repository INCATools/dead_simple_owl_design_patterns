# DOSDP Documentation Generation

DODSP provides automatic documentation generation service for both pattern files and the dosdp schema itself.

### Pattern Documentation

DOSDP provides several CLI interfaces for automatic pattern generation.

```sh
$ dosdp document -i pattern.yaml
$ dosdp document -i pattern.yaml -o pattern.md
$ dosdp document -i pattern.yaml -o 'output folder'

$ dosdp document -i 'pattern folder' -o 'output folder'

$ dosdp document -i pattern.yaml -d 'sample data folder' -o pattern.md
$ dosdp document -i 'pattern folder' -d 'sample data folder' -o 'output folder'
```

A [sample dosdp pattern](https://github.com/obophenotype/cell-ontology/blob/master/src/patterns/dosdp-patterns/cellBearerOfQuality.yaml) and its [auto generated documentation](https://github.com/obophenotype/cell-ontology/blob/master/docs/patterns/cellBearerOfQuality.md) can be seen in the cell ontology.

An additional [overview document](https://github.com/obophenotype/cell-ontology/blob/master/docs/patterns/overview.md) generated to present a summary of the patterns, if a directory is provided as input.

If the optional `sample data folder` parameter is provided, a [data preview](https://github.com/obophenotype/cell-ontology/blob/master/docs/patterns/overview.md#data-preview) is generated in both the pattern and overview documents. To achieve this, the pattern file name and the data file must match.

### DOSDP Schema Documentation

With each version release, DOSDP generates and  publishes a schema documentation. 

```sh
$ dosdp document --schema
$ dosdp document --schema -o <schema.md>
```

Generates md formatted documentation for the [schema](https://github.com/INCATools/dead_simple_owl_design_patterns/tree/master/src/schema/dosdp_schema.md) exists in the dosdp package. An output document location can be optionally identified to specify documentation location or current folder (os current working directory) is used by default.