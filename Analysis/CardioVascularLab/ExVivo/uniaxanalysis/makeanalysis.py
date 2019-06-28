from uniaxanalysis.parsecsv import parsecsv


class makeanalysis(parsecsv):

    def __init__(self, **kwargs):
        super(gensamplesheet, self).__init__(**kwargs)
        a = self.parseNames()
        b = self.dataEntry(a)
        print(self.project)


if __name__ == '__main__':
    # this is a sample to test outputs
    args_dict = {'readfrom': '/home/richard/MyProjects/Analysis/CardioVascularLab/rawData', 'writeto': 'Test',
                 'identifier': '_Fail', 'skiprows': 5, 'ignore': '.tdf', 'project': 'AAA'}
    gensamplesheet(**args_dict)
