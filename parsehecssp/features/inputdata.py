from os import stat
from feature import Feature

class InputData(Feature):
    def __init__(self) -> None:
        self.parts = []
        self.analysisName = None
        self.description = None
        self.dataSetName = None
        self.inputDssFileName = None
        self.dssPathName = None
        self.outputDssFileName = None
        self.projectPath = None
        self.reportFileName = None
        self.analyzeType = None
        self.yearSpecification = None
        self.recordStartDate = None
        self.recordEndDate = None
        self.nDay = []
        self.plottingPositionType = None
        self.probDistType = None
        self.use_log = None
        self.upperConfLevel = None
        self.lowerConfLevel = None
        self.freqs = []
        self.skewOption = None
        self.notes = []

    @staticmethod
    def test(line):
        if line.strip() == '--- Input Data ---':
            return True
        return False

    def import_rpt(self, line, rpt_file):

        while line.strip() != '--- End of Input Data ---':

            if line.split(':')[0] == 'Analysis Name':
                self.analysisName = line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Description':
                self.description = line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Data Set Name':
                self.dataSetName = line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Input DSS File Name':
                self.dssPathName = line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Output DSS File Name':
                self.outputDssFileName = line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Project Path':
                self.projectPath == line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Report File Name':
                self.reportFileName = line.strip().split(':')[-1]
            elif line.split()[0] == 'Analyze':
                self.analyzeType = line.strip().split()[1]
            elif line.split(':')[0] == 'Record Start Date':
                self.recordStartDate = line.strip().split(':')[-1]
            elif line.split(':')[0] == 'Record End Date':
                self.recordEndDate = line.strip().split(':')[-1]
            elif line.strip == 'User-Specified Durations':
                line = next(rpt_file)
                while line.strip() != '':
                    

        


            line = next(rpt_file)
        return next(rpt_file)


