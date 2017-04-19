import glob
listOfFiles = []
for filename in glob.iglob('**/*.py', recursive=True):
    listOfFiles.append(filename)




for lof in listOfFiles:
    with open(lof, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('PyQt5', 'PyQt5')
    filedata = filedata.replace('QtWidgets', 'QtWidgets')

    # Write the file out again
    with open(lof, 'w') as file:
        file.write(filedata)
