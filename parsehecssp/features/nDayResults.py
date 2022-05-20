from ast import Sub
from .feature import Feature, SubFeature
from .utils import split_by_n_str
import re

class EmaData(SubFeature):

    def __init__(self) -> None:
        self.name = None
        self.width = None
        self.header = []
        self.rows = []
        self.years = []
        self.peaks = []
        self.lowValues = []
        self.highValues = []
        self.lowLogValues = []
        self.highLogValues = []
        self.lowThresholds = []
        self.highThresholds = []
        self.lowLogThresholds = []
        self.highLogThresholds = []
        self.types = []
        self.footer = None

    def import_rpt(self, line, rpt_file):
        line = next(rpt_file)
        self.name = line
        line = next(rpt_file)
        self.width = len(line.strip())

        while line != '\n':

            while  not bool(re.match("\d{4}", line[2:6])):
                #Inside Header
                self.header.append(line)
                line = next(rpt_file)

            # Now were are in the table
            print('here')
            while line!= self.header[3]:
                self.rows.append(line)
                parts = line.split()
                self.years.append(parts[1])
                self.peaks.append(parts[2])
                self.lowValues.append(parts[4])
                self.highValues.append(parts[5])
                self.lowLogValues.append(parts[7])
                self.highLogValues.append(parts[8])
                self.lowThresholds.append(parts[10])
                self.highThresholds.append(parts[11])
                self.lowLogThresholds.append(parts[13])
                self.highLogThresholds.append(parts[14])
                self.types.append(parts[16])
                line = next(rpt_file)
            self.footer = line
            line = next(rpt_file)

        return rpt_file

    def __str__(self):
        s = '<< EMA Representation of Data >>\n'
        s+= f'{self.name}\n'
        for line in self.header:
            s+= line
        for row in self.rows:
            s+= row
        s+= self.footer    

        return s

class Moments(SubFeature):

    def __init__(self) -> None:
        super().__init__()

    def import_rpt(self, line, rpt_file):
        return rpt_file
    
    def __str__(self):
        return super().__str__()

class EmpericalData(SubFeature):

    def __init__(self) -> None:
        super().__init__()

    def import_rpt(self, line, rpt_file):
        return rpt_file

    def __str__(self):
        return super().__str__()

class FrequencyCurve(SubFeature):

    def __init__(self) -> None:
        super().__init__()

    def import_rpt(self, line, rpt_file):
        return rpt_file
    
    def __str__(self):
        return super().__str__()


class MGBT(SubFeature):

    def __init__(self) -> None:
        super().__init__()

    def import_rpt(self, line, rpt_file):
        return rpt_file
    
    def __str__(self):
        return super().__str__()


class AnalyticalStats(SubFeature):

    def __init__(self) -> None:
        super().__init__()
    

    def import_rpt(self, line, rpt_file):
        return rpt_file
    
    def __str__(self):
        return super().__str__()

class UserFrequencyCurve(SubFeature):

    def __init__(self) -> None:
        super().__init__()
    
    def import_rpt(self, line, rpt_file):
        return rpt_file
    
    def __str__(self):
        return super().__str__()

class UserStatistics(SubFeature):

    def __init__(self) -> None:
        super().__init__()

    def import_rpt(self, line, rpt_file):
        return rpt_file
    
    def __str__(self):
        return super().__str__()

class Header(SubFeature):
    
    def __init__(self) -> None:
        self.duration = None

    def import_rpt(self, line, rpt_file):
        # line = next(rpt_file)
        self.duration = line.split('-')[0].split()[-1]
        line = next(rpt_file)
        return rpt_file

    def __str__(self):
        s = '============================================================================\n'
        s+= f'Statistical Analysis of {self.duration}-day Maximum values\n'
        s+= '============================================================================\n'
        return super().__str__()


class NDayResult(Feature):

    def __init__(self) -> None:
        self.header = Header()
        self.ema_data = EmaData()
        self.moments = Moments()
        self.empericalData = EmpericalData()
        self.frequencyCurve = FrequencyCurve()
        self.mgbt = MGBT()
        self.analyticalStats = AnalyticalStats()
        self.userFreqCurve = UserFrequencyCurve()
        self.userStats = UserStatistics()
        self.parts = []
    
    @staticmethod
    def test(line):
        if line[:20] == 'Statistical Analysis':
            return True
        return False

    def import_rpt(self, line, rpt_file):
        
        while line[:5] != '=====':
            if line == '\n':
                self.parts.append(line)
            elif line[:20] == 'Statistical Analysis':
                self.header.import_rpt(line, rpt_file)
                self.parts.append(self.header)
            elif line == '<< EMA Representation of Data >>\n':
                self.ema_data.import_rpt(line, rpt_file)
                self.parts.append(self.ema_data)
            elif line[:22] ==   'Fitted log10 Moments':
                self.moments.import_rpt(line, rpt_file)
            else:
                #unknown line
                self.parts.append(line)
            line = next(rpt_file)

        return next(rpt_file)


    def __str__(self):
        return super().__str__()