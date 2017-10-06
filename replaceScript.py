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
