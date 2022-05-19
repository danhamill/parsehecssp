class Header(object):
    def __init__(self) -> None:
        self.analysis_type = None
        self.compute_day = None
        self.comput_month = None
        self.compute_year = None
        self.compute_hour = None
        self.comput_locale = None

    @staticmethod
    def test(line):
        if line[:24] == 'Volume-Duration Analysis':
            return True
        return False

    def import_rpt(self, line, rpt_file):
        self.analysis_type = line.strip()
        line = next(rpt_file)

        self.compute_day = line.split()[0]
        self.compute_month = line.split()[1]
        self.compute_year = line.split()[2]
        self.compute_time = line.split()[3]
        self.compute_locale = line.split()[4]


        return next(rpt_file)

    def __str__(self):
        s = '-----------------------------\n'
        s+= f'{self.analysis_type}\n'
        s+= f'   {self.compute_day} {self.compute_month} {self.compute_year}   {self.compute_time} {self.compute_locale}\n'
        s+= '-----------------------------\n'
        return s