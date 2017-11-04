import shutil
import tempfile


def create_dir(basedir=''):
    """
    Create a unique, temporary directory in /tmp where processing will occur

    Parameters
    ----------
    basedir : str
              The PATH to create the temporary directory in.
    """
    return tempfile.mkdtemp(dir=basedir)


def delete_dir(dir):
    """
    Delete a directory

    Parameters
    ----------
    dir : str
          Remove a directory
    """
    shutil.rmtree(dir)


def file_to_list(file):
    with open(file, 'r') as f:
        file_list = f.readlines()
        file_list = map(str.rstrip, file_list)
        file_list = filter(None, file_list)

    return file_list
