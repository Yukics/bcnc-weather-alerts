import yaml

def load(file):
    with open(file, 'r') as yaml_file:
        conf_loaded = yaml.safe_load(yaml_file)
    return conf_loaded