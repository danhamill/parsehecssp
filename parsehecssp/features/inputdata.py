from .feature import Feature, SubFeature


class Durations(SubFeature):

    def __init__(self) -> None:
        self.ndays = []

    def import_rpt(self, line, rpt_file):
        while line != '\n':
            _nday = line.strip().split(':')[-1].split()[0]
            self.ndays.append(_nday)
            line = next(rpt_file)
        return rpt_file

    def __str__(self):
        s = 'User-Specified Durations\n'
        for nday in self.ndays:
            if int(nday) == 1:
                s+= f'   Duration:   {nday} day\n'
            elif int(nday) < 10:
                s+= f'   Duration:   {nday} days\n'
            elif int(nday)<100:
                s+= f'   Duration:  {nday} days\n'
            else:
                s+= f'   Duration: {nday} days\n'
        s+='\n'
        return s

class Frequencies(SubFeature):

    def __init__(self) -> None:
        self.freqs = [] 

    def import_rpt(self, line, rpt_file):
        while line != '\n':
            _freq = line.strip().split(':')[-1].split()[0]
            self.freqs.append(_freq)
            line = next(rpt_file)
        return rpt_file

    def __str__(self):
        s = 'User-Specified Frequencies\n'
        for freq in self.freqs:
            s+= f'   Frequency: {freq}\n'
        s+='\n'
        return s
    
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
        self.durations = Durations()
        self.plottingPositionType = None
        self.probDistType = None
        self.upperConfLevel = None
        self.lowerConfLevel = None
        self.freqs = Frequencies()
        self.skewOption = None

    @staticmethod
    def test(line):
        if line.strip() == '--- Input Data ---':
            return True
        return False

    def import_rpt(self, line, rpt_file):

        while line.strip() != '--- End of Input Data ---':
            if line == '\n':
                self.parts.append(line)
            elif line.split(':')[0] == 'Analysis Name':
                self.analysisName = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Description':
                self.description = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Data Set Name':
                self.dataSetName = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Input DSS File Name':
                self.dssPathName = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Output DSS File Name':
                self.outputDssFileName = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'DSS Pathname':
                self.projectPath == line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Report File Name':
                self.reportFileName = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split()[0] == 'Analyze':
                self.analyzeType = line.strip().split()[1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Record Start Date':
                self.recordStartDate = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Record End Date':
                self.recordEndDate = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.strip() == 'User-Specified Durations':
                line = next(rpt_file)
                self.durations.import_rpt(line, rpt_file)
                self.parts.append(self.durations)
            elif line.split(':')[0] == 'Plotting Position Type':
                self.plottingPositionType = line.strip().split(':')[-1]
                self.parts.append(line)
            elif line.split(':')[0] == 'Probability Distribution Type':
                self.probDistType = line.strip().split(':')[-1]
                self.parts.append(line)        
            elif line.split(':')[0] == 'Upper Confidence Level':
                self.upperConfLevel = line.strip().split(':')[-1]
                self.parts.append(line)               
            elif line.split(':')[0] == 'Lower Confidence Level':
                self.lowerConfLevel = line.strip().split(':')[-1]
                self.parts.append(line)   
            elif line.strip() == 'User-Specified Frequencies':
                line = next(rpt_file)
                self.freqs.import_rpt(line, rpt_file)
                self.parts.append(self.freqs)             
            else:
                self.parts.append(line)
            line = next(rpt_file)
        return rpt_file

    def __str__(self):
        s = ''
        for line in self.parts:
            s+=str(line)
        s+='--- End of Input Data ---\n'

        return s
