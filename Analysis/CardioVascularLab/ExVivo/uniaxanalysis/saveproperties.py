import csv
import os.path


def write_props_csv(fname, propDict, sample, headers):
    if not os.path.isfile(fname):

        with open(fname, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerow([propDict[sample][h] for h in headers])
    else:
        with open(fname, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([propDict[sample][h] for h in headers])
