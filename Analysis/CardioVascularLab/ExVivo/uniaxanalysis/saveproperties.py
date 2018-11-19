import csv
import os.path


def write_props_csv(fname, propsList):
    if not os.path.isfile(fname):
        headers = ['Sample', 'Stiffness (MPa)', 'Strength (MPa)']
        with open(fname, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow(propsList)
    else:
        with open(fname, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(propsList)
