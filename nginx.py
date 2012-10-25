import re, sys
from utils import print_with_color

DETAILS_STATUS = [
    '404',
    '500',
]


class NginxUtil:
    re = ' '.join([
        '(\d+\.\d+\.\d+\.\d+)',
        '- -',
        '(\[.*\])',
        '"(.*)"',
        '(\d+) \d',
    ])
    stats = {
        'ip': {},
        'status_codes': {},
        '404_details': {},
        '500_details': {},
    }
    
    def parse_line(self, line):
        s = re.search(NginxUtil.re, line)
        if s:
            ip = s.group(1)
            if ip in self.stats['ip']:
                self.stats['ip'][ip] += 1
            else:
                self.stats['ip'][ip] = 1

            status = s.group(4)
            if status in self.stats['status_codes']:
                self.stats['status_codes'][status] += 1
            else:
                self.stats['status_codes'][status] = 1
            
            if status in DETAILS_STATUS:
                label = '%s_details' % status
                url = re.search('[A-Z]+ (.*) ', s.group(3)).group(1)

                if label in self.stats:
                    if url in self.stats[label]:
                        self.stats[label][url] += 1
                    else:
                        self.stats[label][url] = 1
                else:
                    self.stats[label] = { url: 1 }

    def print_stats(self):
        for code in self.stats['status_codes']:
            label = '%s_details' % code
            print 'Number of %s-responses: %s' % (code, self.stats['status_codes'][code])
            if label in self.stats:
                print 'Details: %s' % self.stats[label]


def main():
    analyzer = NginxUtil()
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        print_with_color('To few arguments', 'red')
        return

    with open(fname) as f:
        content = f.readlines()
    for line in content:
        analyzer.parse_line(line)

    analyzer.print_stats()

if __name__ == "__main__":
    main()
