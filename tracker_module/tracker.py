import os
import platform
import sys
import getopt
import json
import time
import signal
from ConfigParser import SafeConfigParser

from os import listdir
from os.path import isfile, join
from datetime import datetime

class Tracker(object):

    update_state_msg         = "Updating current state ~>"
    update_json_msg          = "JSON update initiated ~>"
    update_tracked_files_msg = "Updating list of files, that are tracked ~>"
    write_to_storage_msg     = "Writing to storage file ~>"
    run_shell_command_msg    = "Executing commands ~>"
    no_update_msg            = "No changes in tracked files, so shell commands won't be executed"
    shutting_down_msg        = "Shutting down the tracker"

    EXIT_CODE                = 0

    """ Variable holder """
    def __init__(self, path_to_setup):
        signal.signal(signal.SIGTERM, self.shut_down)

        config = SafeConfigParser()

        if isfile(path_to_setup):
            config.read(path_to_setup)
        else:
            self.shut_down(msg='No configuration file found')

        self.path_to_files    = [path.strip() for path in config.get('main', 'dirs_to_track').split(',')]
        self.path_to_storage  = config.get('main', 'storage_file')
        self.path_to_log      = config.get('main', 'log_file')
        self.update_interval  = config.getint('main', 'update_interval')
        self.execute_commands = [command.strip() for command in config.get('main', 'execute_commands').split(',')]
        self.tracked_files    = []
        self.triggered        = False
        self.current_state    = {}

        if isfile(self.path_to_storage):
            data = {}
            with open(self.path_to_storage, 'r') as js:
                data = json.load(js)

            for key in data.iterkeys():
                self.tracked_files.append(key)

            self.current_state = data
        else:
            self.tracked_files   = [[join(path, file) for file in listdir(path) if isfile(join(path, file))] for path in self.path_to_files]
            self.tracked_files   = [file for sublist in self.tracked_files for file in sublist]

    def creation_date(self, path_to_file):
        """ PRIVATE
        Try to get the date that a file was created(modified)
        """
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)

        stat = os.stat(path_to_file)
        return stat.st_mtime

    def write_to_log(self, *arg):
        """ PRIVATE
        Writes output to log file
        """
        output = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " => " + ' '.join(arg) + '\n'
        with open(self.path_to_log, 'a') as f:
            f.write(output)

    def update_json(self, new_data):
        """ PRIVATE
        Updates existing storage json file
        """
        old_data = {}
        with open(self.path_to_storage, 'r') as js:
            old_data = json.load(js)

        for key, value in new_data.iteritems():
            old_data[key] = value

        with open(self.path_to_storage, 'w') as js:
            json.dump(old_data, js)

        self.write_to_log(self.update_json_msg, str(old_data))

    def update_happend(self):
        """ PRIVATE
        Checks if any of the files were changed
        """
        old_data = {}
        with open(self.path_to_storage, 'r') as js:
            old_data = json.load(js)

        if cmp(self.current_state, old_data) == 0:
            self.triggered = False
        else:
            self.triggered = True

    def shut_down(self, signum='', frame='', msg=''):
        """ PRIVATE
        Gracefully shuts tracker
        """
        if msg:
            print "\n" + msg
            self.write_to_log(msg)
        else:
            print "\n" + self.shutting_down_msg
            self.write_to_log(self.shutting_down_msg)

        try:
            sys.exit(self.EXIT_CODE)
        except SystemExit as err:
            if err.code != self.EXIT_CODE:
                raise
            else:
                os._exit(self.EXIT_CODE)


    def write_to_storage(self):
        if isfile(self.path_to_storage):
            self.update_json(self.current_state)
        else:
            with open(self.path_to_storage, 'w') as js:
                json.dump(self.current_state, js)

                self.write_to_log(self.write_to_storage_msg, str(self.current_state))

    def update_current_state(self):
        for file in self.tracked_files:
            self.current_state[file] = self.creation_date(file)

        self.write_to_log(self.update_state_msg, str(self.current_state))

    def update_tracked_files_list(self):
        file_list = [[join(path, file) for file in listdir(path) if isfile(join(path, file))] for path in self.path_to_files]
        file_list = [file for sublist in self.tracked_files for file in sublist]

        new_files = list(set(file_list) - set(self.tracked_files))
        self.tracked_files = self.tracked_files + new_files

        self.write_to_log(self.update_tracked_files_msg, new_files)

    def run_shell_command(self):
        for command in self.execute_commands:
            os.system(command)

        self.write_to_log(self.run_shell_command_msg, str(self.execute_commands))

    def run_tracker(self):
        try:
            self.update_current_state()
            self.write_to_storage()
            while True:
                if self.triggered:
                    self.write_to_storage()

                time.sleep(self.update_interval)
                self.write_to_log("Looking for updates...")

                self.update_current_state()

                self.update_happend()
                if self.triggered:
                    self.run_shell_command()
                else:
                    self.write_to_log(self.no_update_msg)
        except KeyboardInterrupt:
            self.shut_down()
