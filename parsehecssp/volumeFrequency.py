from ast import In
from .features.header import Header
from .features.inputdata import InputData
from .features.nDayResults import EmpiricalData, NDayResult
import os.path

class ParseVolumeFrequency(object):
    def __init__(self, rpt_filename) -> str:
        self.analysis_parts = []

        with open(rpt_filename, 'rt') as rpt_file:
            next(rpt_file)
            for line in rpt_file:

                if line == '\n':
                    self.analysis_parts.append(line)
                elif Header.test(line):
                    hh = Header()
                    hh.import_rpt(line, rpt_file)
                    self.analysis_parts.append(hh)
                elif InputData.test(line):
                    id = InputData()
                    id.import_rpt(line, rpt_file)
                    self.analysis_parts.append(id)
                elif NDayResult.test(line):
                    nd = NDayResult()
                    nd.import_rpt(line, rpt_file, id.durations.ndays[-1])
                    self.analysis_parts.append(nd)
                else:
                    if line != '============================================================================\n':
                        #Unknown line
                        self.analysis_parts.append(line)

    def write(self, out_rpt_filename):

        with open(out_rpt_filename, 'w') as outfile:
            for line in self.analysis_parts:
                outfile.write(str(line))

    def getNDayCurves(self):

        nDayResults = [item.frequencyCurve.computedCurve for item in self.analysis_parts if isinstance(item, NDayResult)]

        return nDayResults

    def getEmpericalData(self):

        empericalResults = [item.empiricalData.orderedEvents for item in self.analysis_parts if isinstance(item, NDayResult)]

        return empericalResults

