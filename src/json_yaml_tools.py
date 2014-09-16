import yaml
import json

def load_yaml_from_file(filePath):
    f = open(filePath, "r")
    y = yaml.load(f)
    f.close()
    return y

def load_json_from_file(path):
    json_file = open(path, "r")
    json_string = json_file.read()
    json_file.close()
    return json.loads(json_string)

def yaml2json(YamlFilePath, JsonFilePath):
    """Convert YAML file to JSON file""" 
    pdm = load_yaml_from_file(YamlFilePath)
    j = open(JsonFilePath, "w")
    j.write(json.dumps(pdm, sort_keys=True, indent=4))
    j.close()
