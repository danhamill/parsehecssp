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
        s+= f'{self.name}'
        for line in self.header:
            s+= line
        for row in self.rows:
            s+= row
        s+= self.footer  
        s+= '\n'  

        return s

class Moments(SubFeature):

    def __init__(self) -> None:
        self.rows = []
        self.emaSiteWithOutRegional = dict.fromkeys(['mean','variance','stDev','skew'])
        self.emaWithRegionalAndB17bMSE = dict.fromkeys(['mean','variance','stDev','skew'])
        self.emaWithRegionalAndSepcifMSE = dict.fromkeys(['mean','variance','stDev','skew'])
        self.emaEstimateMSE = None
        self.mseAtSite = None
        self.erlAtSite = None
        self.erlSystHistnoOutlier = None
        self.erlCohn1997 = None
        self.grubbCritValue = None
        self.numYearNonInfThresholds = None


    def import_rpt(self, line, rpt_file):
        
        while line.strip() != '--- Final Results ---':
            if line == '\n':
                self.rows.append(line)
            elif line[:36] == '  EMA at-site data w/o regional info':
                chunks = line.strip().split()[-4:]
                self.emaSiteWithOutRegional = dict(zip(self.emaSiteWithOutRegional, chunks))
                self.rows.append(line)
            elif line[:38] == '  EMA w/ regional info and B17b MSE(G)':
                chunks = line.strip().split()[-4:]
                self.emaWithRegionalAndB17bMSE = dict(zip(self.emaWithRegionalAndB17bMSE, chunks))
                self.rows.append(line)               
            elif line[:43] == '  EMA w/ regional info and specified MSE(G)':
                chunks = line.strip().split()[-4:]
                self.emaWithRegionalAndSepcifMSE = dict(zip(self.emaWithRegionalAndSepcifMSE, chunks))
                self.rows.append(line)
            elif line[:32] == '  EMA Estimate of MSE[G at-site]':
                self.emaEstimateMSE = line.strip().split()[-1]
                self.rows.append(line)
            elif line[:27] == '  MSE[G at-site systematic]':
                self.mseAtSite = line.strip().split()[-1]
                self.rows.append(line)
            elif line[:38] == '  Equivalent Record Length [G at-site]':
                self.erlAtSite = line.strip().split()[-1]
                self.rows.append(line)
            elif line[:46] == '  Equivalent Record Length [Syst+Hist-LowOutl]':
                self.erlSystHistnoOutlier = line.strip().split()[-1]
                self.rows.append(line)
            elif line[:46] == '  Equivalent Record Length [Cohn et al (1997)]':
                self.erlCohn1997 = line.strip().split()[-1]
                self.rows.append(line)
            elif line[:28] == '  Grubbs-Beck Critical Value':
                self.grubbCritValue = line.strip().split()[-1]
                self.rows.append(line)
            elif line[:35] == '  # Years w/ non [0-inf] Thresholds':
                self.numYearNonInfThresholds = line.strip().split()[-1]
                self.rows.append(line)
            else:
                self.rows.append(line)

            line = next(rpt_file)

        self.rows.append(line)
        return rpt_file
    
    def __str__(self):
        s = ''

        for row in self.rows:
            s += row
        # s+='\n'

        return s

class EmpiricalData(SubFeature):

    def __init__(self) -> None:
        self.rows = []
        self.events = {}
        self.orderedEvents= {}


    def import_rpt(self, line, rpt_file, duration):

        # Header
        while not bool(re.match("\d{4}", line[10:14])):
            self.rows.append(line)
            line = next(rpt_file) 

        # Table
        while line[:6] != '|-----':
            chunks = line.split()
            self.events.update({''.join(chunks[1:4]): chunks[4]})
            self.orderedEvents.update({chunks[6]:{'wy': chunks[7],
                                                   'flow': chunks[8],
                                                   'hsPlotPos': chunks[9],
                                                   'n-day': f'{duration.zfill(2)}-day'}
                                        })
            self.rows.append(line)
            line = next(rpt_file)
        
        # Footer
        while line != '\n':
            self.rows.append(line)
            line = next(rpt_file)

        self.rows.append(line)
        return rpt_file

    def __str__(self):

        s = ''
        for row in self.rows:
            s += row
        return s

class FrequencyCurve(SubFeature):

    def __init__(self):
        self.rows = []
        self.computedCurve = {}
        # self.upperConf = {}
        # self.lowerConf = {}



    def import_rpt(self, line, rpt_file, duration):

        table_delim = '|------------------------------|-------------|-----------------------------|'
        while line.strip() != table_delim:
            self.rows.append(line)
            line = next(rpt_file)

        self.rows.append(line)
        line = next(rpt_file)
        while line.strip() != table_delim:
            chunks = line.split()

            pctExceedance = chunks[4]

            self.computedCurve.update({pctExceedance:{'flow':chunks[1],
                                                      'variance':chunks[2],
                                                      'uppperConf': chunks[-3],
                                                      'lowerConf': chunks[-2],
                                                      'n-day': f'{duration.zfill(2)}-day'
                                                      }
                                      })
            # self.upperConf.update({pctExceedance:chunks[-3]})
            # self.lowerConf.update({pctExceedance:chunks[-2]})
            self.rows.append(line)
            line = next(rpt_file)
        self.rows.append(line)
        
        return rpt_file
    
    def __str__(self):
        s = ''
        for row in self.rows:
            s += row
        return s


class MGBT(SubFeature):

    def __init__(self) -> None:
        self.rows = []
        self.mgbt_table = {}


    def import_rpt(self, line, rpt_file):
        
        table_delim = '|----------------|-------------|'
        while line.strip() != table_delim:
            self.rows.append(line)
            line = next(rpt_file)
        
        self.rows.append(line)
        line = next(rpt_file)

        while line.strip() != table_delim:
            chunks= line.split()
            self.mgbt_table.update({chunks[1]:chunks[-2]})
            self.rows.append(line)
            line = next(rpt_file)

        self.rows.append(line)


        return rpt_file
    
    def __str__(self):
        s = ''
        for row in self.rows:
            s += row
        return s


class AnalyticalStats(SubFeature):

    def __init__(self) -> None:
        self.rows = []
        self.stats = {}
        self.num_events = {}
    

    def import_rpt(self, line, rpt_file):
        table_delim = '|------------------------------|-------------------------------|'

        while line.strip() != table_delim:
            self.rows.append(line)
            line = next(rpt_file)

        self.rows.append(line)
        line = next(rpt_file)

        while line.strip() != table_delim:

            # Find indices of pipes in string
            col_idx = [i for i in range(len(line)) if line.startswith('|', i)]
            
            left_table = line[1:col_idx[1]].strip().split()
            self.stats.update({' '.join(left_table[:-1]):left_table[-1]})

            right_table = line[col_idx[1]+1:].strip().split()[:-1]
            self.num_events.update({' '.join(right_table[:-1]):right_table[-1]})
            self.rows.append(line)

            line = next(rpt_file)
        
        self.rows.append(line)
        
        return rpt_file
    
    def __str__(self):
        s = ''
        for row in self.rows:
            s += row
        return s


class UserFrequencyCurve(SubFeature):

    def __init__(self) -> None:
        self.rows = []
        self.computedCurve = {}
        self.upperConf = {}
        self.lowerConf = {}


    def import_rpt(self, line, rpt_file):

        table_delim = '|------------------------------|-------------|-----------------------------|'
        while line.strip() != table_delim:
            self.rows.append(line)
            line = next(rpt_file)

        self.rows.append(line)
        line = next(rpt_file)
        while line.strip() != table_delim:
            chunks = line.split()

            pctExceedance = chunks[4]

            self.computedCurve.update({pctExceedance:{'flow':chunks[1],
                                                      'variance':chunks[2]}
                                      })
            self.upperConf.update({pctExceedance:chunks[-3]})
            self.lowerConf.update({pctExceedance:chunks[-2]})
            self.rows.append(line)
            line = next(rpt_file)
        self.rows.append(line)
        
        return rpt_file
    
    def __str__(self):
        s = ''
        for row in self.rows:
            s += row
        return s

class UserStatistics(SubFeature):

    def __init__(self) -> None:
        self.rows = []
        self.stats = {}
        self.num_events = {}
    

    def import_rpt(self, line, rpt_file):
        table_delim = '|------------------------------|-------------------------------|'

        while line.strip() != table_delim:
            self.rows.append(line)
            line = next(rpt_file)

        self.rows.append(line)
        line = next(rpt_file)

        while line.strip() != table_delim:

            # Find indices of pipes in string
            col_idx = [i for i in range(len(line)) if line.startswith('|', i)]
            
            left_table = line[1:col_idx[1]].strip().split()
            if len(left_table)>0:
                self.stats.update({' '.join(left_table[:-1]):left_table[-1]})

            right_table = line[col_idx[1]+1:].strip().split()[:-1]
            if len(right_table)>0:
                self.num_events.update({' '.join(right_table[:-1]):right_table[-1]})
            self.rows.append(line)

            line = next(rpt_file)
        
        self.rows.append(line)
        
        return rpt_file
    
    def __str__(self):
        s = ''
        for row in self.rows:
            s += row
        return s


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
        return s


class NDayResult(Feature):

    def __init__(self) -> None:
        self.header = Header()
        self.ema_data = EmaData()
        self.moments = Moments()
        self.empiricalData = EmpiricalData()
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

    def import_rpt(self, line, rpt_file, max_dur):
        
        while line[:5] != '=====':
            if line == '\n':
                self.parts.append(line)
            elif line[:20] == 'Statistical Analysis':
                self.header.import_rpt(line, rpt_file)
                self.parts.append(self.header)
                if self.header.duration == max_dur:
                    print('here')
            elif line == '<< EMA Representation of Data >>\n':
                self.ema_data.import_rpt(line, rpt_file)
                self.parts.append(self.ema_data)
            elif line[:22] == '  Fitted log10 Moments':
                self.moments.import_rpt(line, rpt_file)
                self.parts.append(self.moments)
            elif line.strip() == '<< Plotting Positions >>':
                self.empiricalData.import_rpt(line, rpt_file, self.header.duration)
                self.parts.append(self.empiricalData)
            elif line.strip() == '<< Frequency Curve >>':
                self.frequencyCurve.import_rpt(line, rpt_file, self.header.duration)
                self.parts.append(self.frequencyCurve)
            elif line.strip() == '<< Multiple Grubbs-Beck Test P-Values >>':
                self.mgbt.import_rpt(line, rpt_file)
                self.parts.append(self.mgbt)
            elif line[:23] == '|        Log Transform:':
                self.analyticalStats.import_rpt(line, rpt_file)
                self.parts.append(self.analyticalStats)
            elif line.strip() == '<< User Frequency Curve >>':
                self.userFreqCurve.import_rpt(line, rpt_file)
                self.parts.append(self.userFreqCurve)
                # self.parts.append(line)
            elif line.strip() == '<< User Statistics >>':
                self.userStats.import_rpt(line, rpt_file)
                self.parts.append(self.userStats)
                if self.header.duration == max_dur:
                    return
            else:
                #unknown line
                self.parts.append(line)

            line = next(rpt_file)
            # self.parts.append(line)

        return rpt_file


    def __str__(self):
        s = ''

        for line in self.parts:
            s+= str(line)

        return s