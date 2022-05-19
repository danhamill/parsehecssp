import os
import sys

sys.path.insert(0, os.path.abspath('.'))
import parsehecssp as phsp

def main():

    rpt_filename = r'tests\Unreg_Flow_Rio_Grande_Test_10.rpt'


    rpt = phsp.volumeFrequency.ParseVolumeFrequency(rpt_filename)


if __name__ == '__main__':
    main()