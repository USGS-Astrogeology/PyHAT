try:
    import yaml
except:
    print('YAML package not installed, disabling yaml_io module')


def read_yaml(inputfile):
    """
    Read the input yaml file into a python dictionary

    Parameters
    =========
    inputfile : str
                PATH to the file on disk

    Returns
    =======
    ydict : dict
            YAML file parsed to a Python dict
    """
    try:
        with open(inputfile, 'r') as f:
            ydict = yaml.load(f)
    except:  # pragma: no cover
        raise IOError('Unable to load YAML file.')
    return ydict
