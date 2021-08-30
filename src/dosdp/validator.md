# DOSDP Validator

DOSDP provides a validation interface for both CLI and Python.

### From the CLI

```sh
$ dosdp validate -i <test.yaml or 'test folder'>
```

### From Python

```python
from dosdp import validator

validator.validate("test.yaml")
```

DOSDP validates given argument if it is a yaml/yml file. If argument is a folder, validates all pattern files located in the given directory.

### Validation Steps

1. Test converstion of YAML to JSON
2. Validate against JSON schema (e.g. see [dosdp_schema.md](https://github.com/INCATools/dead_simple_owl_design_patterns/tree/master/src/schema/dosdp_schema.md) and [dosdp_schema.yaml](https://github.com/INCATools/dead_simple_owl_design_patterns/tree/master/src/schema/dosdp_schema.yaml))
3. Test that all var names in printf statements are valid (declared) for the pattern
4. Checks quoted names in the printf_owl field correspond to dictionary entries in the pattern.