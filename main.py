import sys
import getopt

from tracker_module import Tracker

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "s:")
    except getopt.GetoptError:
        print 'python tracker.py -s <path_to_setup_file> '
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python tracker.py -s <path_to_setup_file> '
            sys.exit()
        elif opt in ("-s", "--setup"):
            # print arg
            tracker = Tracker(arg)
            tracker.run_tracker()

if __name__ == "__main__":
    main(sys.argv[1:])
