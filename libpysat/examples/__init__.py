import os

import libpysat

__all__ = ['get_path']

# Used largely unmodififed from:
# https://github.com/pysal/pysal/blob/master/pysal/examples/__init__.py

base = os.path.split(libpysat.__file__)[0]
example_dir = os.path.join(base, 'examples')
dirs = next(os.walk(example_dir))[1]
file_2_dir = {}

for d in dirs:
    tmp = os.path.join(example_dir, d)
    file_in_tmp = os.listdir(tmp)
    for f in file_in_tmp:
        file_2_dir[f] = tmp


def get_path(example_name):  # pragma: no cover
    """
    Get the path of the example file

    Parameters
    ==========
    example_name : str
                   The name of the example file to return the absolute path
    """
    if not isinstance(example_name, str):
        try:
            example_name = str(example_name)
        except:
            raise KeyError('Cannot coerce requested example name to string')
    if example_name in dirs:
        return os.path.join(example_dir, example_name)
    elif example_name in file_2_dir:
        d = file_2_dir[example_name]
        return os.path.join(d, example_name)
    elif example_name == "":
        return os.path.join(base, 'examples', example_name)
    else:
        raise KeyError(example_name + ' not found in built-in examples')


def available(directory='', verbose=False):  # pragma: no cover
    """
    List available datasets in autocnet.examples

    Parameters
    ==========
    directory : str
                The directory in which examples are stored

    verbose : boolean
              If True, return README information about each example, default False
    """
    base = get_path(directory)
    examples = [os.path.join(get_path(''), d) for d in os.listdir(base)]
    if directory != '':
        examples = [d for d in examples if '__' not in d]
    else:
        examples = [d for d in examples if os.path.isdir(d) and '__' not in d]
    # if not verbose:
    return [os.path.split(d)[-1] for d in examples]
    # examples = [os.path.join(dty, 'README.md') for dty in examples]
    # descs = [_read_example(path) for path in examples]
    # return [{desc['name']:desc['description'] for desc in descs}]
