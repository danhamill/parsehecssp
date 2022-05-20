from ast import In
from .features.header import Header
from .features.inputdata import InputData
from .features.nDayResults import NDayResult
import os.path

class ParseVolumeFrequency(object):
    def __init__(self, rpt_filename) -> str:
        self.analysis_parts = []

        with open(rpt_filename, 'rt') as rpt_file:
            next(rpt_file)
            for line in rpt_file:
                if Header.test(line):
                    hh = Header()
                    hh.import_rpt(line, rpt_file)
                    self.analysis_parts.append(hh)
                elif InputData.test(line):
                    id = InputData()
                    id.import_rpt(line, rpt_file)
                    self.analysis_parts.append(id)
                elif NDayResult.test(line):
                    nd = NDayResult()
                    nd.import_rpt(line, rpt_file)
                    self.analysis_parts.append(nd)
                else:
                    #Unknown line
                    self.analysis_parts.append(line)

    def write(self, out_rpt_filename):

        with open(out_rpt_filename, 'w') as outfile:
            for line in self.analysis_parts:
                outfile.write(str(line))