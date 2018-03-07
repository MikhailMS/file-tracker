import unittest
import os
import sys
from os.path import join
from tracker import Tracker
from ConfigParser import SafeConfigParser

class TestTrackerMethods(unittest.TestCase):
    def test_init(self):
        config_path = join(sys.path[0], 'test_config.ini')
        tracker = Tracker(config_path)

        config = SafeConfigParser()
        config.read(config_path)
        paths            = [path.strip() for path in config.get('main', 'dirs_to_track').split(',')]
        storage          = config.get('main', 'storage_file')
        log              = config.get('main', 'log_file')
        update_interval  = config.getint('main', 'update_interval')
        execute_commands = [command.strip() for command in config.get('main', 'execute_commands').split(',')]

        self.assertEqual(tracker.path_to_files, paths)
        self.assertEqual(tracker.path_to_storage, storage)
        self.assertEqual(tracker.path_to_log, log)
        self.assertEqual(tracker.update_interval, update_interval)
        self.assertEqual(tracker.execute_commands, execute_commands)
        self.assertEqual(tracker.tracked_files, [])
        self.assertEqual(tracker.triggered, False)
        self.assertEqual(tracker.current_state, {})

    def test_creation_date(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

        new_file_path = join(sys.path[0], 'test_creation_date.txt')
        with open(new_file_path, 'a') as f:
            f.write("")

        stat = os.stat(new_file_path)
        self.assertEqual(stat.st_mtime, tracker.creation_date(new_file_path))

    def test_write_to_log(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))
        tracker.write_to_log("Test message")

        lines = ""
        with open(tracker.path_to_log, 'r') as log:
            lines = log.read()

        self.assertTrue('Test message' in lines)

    def test_update_json(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))


    def test_update_happend(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

    def test_write_to_storage(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

    def test_update_current_state(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

    def test_update_tracked_files_list(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

    def test_run_shell_command(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

    def test_run_tracker(self):
        tracker = Tracker(join(sys.path[0], 'test_config.ini'))

if __name__ == '__main__':
    unittest.main()
