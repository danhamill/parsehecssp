import os
import sys
import filecmp

sys.path.insert(0, os.path.abspath('.'))
import parsehecssp as phsp

def check_files(out_file, rpt_filename):
    # reading files
    f1 = open(out_file, "r")  
    f2 = open(rpt_filename, "r")  
    
    i = 0
    output = []
    for line1 in f1:
        i += 1
        for line2 in f2:
            # matching line1 from both files
            if line1 == line2:  
                pass
            else:
                output.append(["Line ", i, ":"])
            break
    
    # closing files
    f1.close()                                       
    f2.close() 
    return output

def main():
    out_file = r'tests\testVolFreq.out'
    rpt_filename = r'tests\Sinnemahoning_VolumeFrequency.rpt'


    rpt = phsp.volumeFrequency.ParseVolumeFrequency(rpt_filename)
    rpt.write(out_file)

    output = check_files(out_file, rpt_filename)
    if len(output) ==0:
        print('Files are identical')
    else: 
        print('files are not identical')


if __name__ == '__main__':
    main()