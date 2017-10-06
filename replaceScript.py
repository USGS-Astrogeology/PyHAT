import glob

listOfFiles = []
for filename in glob.iglob('**/*.py', recursive=True):
    with open(filename, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('', '')

    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)

import os

user_input = './'
directory = os.listdir(user_input)

searchstring = input('What word are you trying to find?')

for filename in glob.iglob('**/*.py', recursive=True):
    with open(filename, 'r') as file:
        filedata = file.read()

        if searchstring in filedata:
            print('found string in file %s' % filename)
        file.close()
