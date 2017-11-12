from socket import socket
from sys import argv


class Target:
    def __init__(self, text, ip, ports):
        """ Constructor """
        # Comment, ip target, ports (as list) and result (as list)
        self.text = text
        self.ip = ip
        self.ports = ports.split(',')
        self.result = list()

    def test(self):
        """
         Test ip and ports.
        :return: Fill result list
        """

        for port in self.ports:
            s = socket()
            s.settimeout(3)
            try:
                print 'Testing {} {}:{} ...'.format(self.text, self.ip, port),
                s.connect((self.ip, int(port)))
                self.result.append((self.text, self.ip, port, 'OK'))
                print 'OK'
            except Exception as e:
                self.result.append((self.text, self.ip, port, 'KO'))
                print 'KO'

    def show_results(self):
        """
        Format data result of this target
        :return: string with results of this target
        """
        # return output
        return '\n'.join('{} {} {} {}'.format(str(x[0]), str(x[1]), str(x[2]), str(x[3])) for x in self.result)

    def __str__(self):
        return '{} {} {}'.format(self.text, self.ip, self.ports)

def read_file(config_file):
    """
    Read config file passed as argument. This config file has the following data:
    Text;IP;Ports separated by ,
    SERVER 1;192.168.10.100;22,80,8080,20000
    """
    lines = []
    with open(config_file, 'r') as f:
        for line in f.readlines():
            text, ip, ports = line.strip().split(';')
            lines.append(Target(text, ip, ports))

    return lines


# Recover arguments config_file and report_file
config_file = argv[1]
report_file = argv[2]

# Read configuration
targets = read_file(config_file)

# Test all targets
for target in targets:
    target.test()

# Generate reports
report_data = list()
for target in targets:
    report_data.append(target.show_results())

# Generate report file
report_file_handler = open(report_file, 'w')
report_file_handler.write('\n'.join(report_data))
report_file_handler.close()
