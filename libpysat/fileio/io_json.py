import json


def read_json(inputfile):
    """
    Read the input json file into a python dictionary.

    Parameters
    ==========
    inputfile : str
                PATH to the file on disk

    Returns
    =======
    jobs : dict
           returns a dictionary 

    >>> inputs = readinputfile('testfiles/sampleinput.json')
    >>> k = inputs.keys()
    >>> k.sort()
    >>> print k
    [u'ancillarydata', u'bands', u'force', u'images', u'latlon', u'name', u'outputformat', u'processing_pipeline', u'projection', u'resolution', u'rtilt', u'tesatm', u'uddw']

    """
    with open(inputfile, 'r') as f:
        try:
            jdict = json.load(f)
            return jdict
        except IOError:  # pragma: no cover
            return


def write_json(outdata, outputfile):
    """
    Write a Python dictionary as a plain-text JSON file

    Parameters
    ==========
    outdata : dict
              The data structure to be serialized
    outputfile : str
                 The file to write the data to.
    """
    try:
        with open(outputfile, 'w') as f:
            f.write(json.dumps(outdata, outputfile))
    except:  # pragma: no cover
        raise IOError('Unable to write data to {}'.format(outputfile))
