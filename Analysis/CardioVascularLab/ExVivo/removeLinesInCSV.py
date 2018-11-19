import glob

myfiles = glob.glob('*.csv')

for file in myfiles:
    lines = open(file).readlines()
    open(file, 'w').writelines(lines[3:])
