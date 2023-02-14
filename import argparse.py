import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Parse command line arguments.')
    parser.add_argument('--debug', dest='debugmode', type=str, choices=['ON', 'OFF'], default='OFF', help='Turn debugging function ON or OFF')
    parser.add_argument('--log',   dest='logmode',   type=str, choices=['ON', 'OFF'], default='OFF', help='The name of the log file')
    parser.add_argument('--o',     dest='logfile',   type=str, default='fix_subs.log', help='The name of the log file')
    parser.add_argument('--loglevel', dest='loglevel', type=str, choices=['INFO', 'VERBOSE','ERROR'], help='The type of information to print')
    parser.add_argument('--demo', action='store_true', default=False, help='Turn on demo mode')

    return parser.parse_args()

def main(args):
    print('debug:', args.debugmode)
    print('log:', args.logmode,' logfile:',args.logfile)
    print('loglevel:', args.loglevel)
    print('demo:', args.demo)

if __name__ == '__main__':
    args = parse_args()
    main(args)