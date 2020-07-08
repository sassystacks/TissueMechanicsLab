
from uniaxanalysis.parsecsv import parsecsv

class DataInterfacer:

    def __init__(self, classList=[], sampleList=[]):

        self.classList = classList
        self.sampleList = sampleList
        self._SetSampleList()

    def _SetSampleList(self):
        for c in self.classList:
            c.sampleList = self.sampleList
