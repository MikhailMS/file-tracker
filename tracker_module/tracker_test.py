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
        paths = [path.strip() for path in config.get('main', 'dirs_to_track').split(',')]

        self.assertEqual(tracker.path_to_files, paths)
        self.assertEqual(tracker.path_to_storage, 'storage.json')
        self.assertEqual(tracker.path_to_log, 'progress-log')
        self.assertEqual(tracker.update_interval, 5)
        self.assertEqual(tracker.execute_commands, ["echo 'Update'"])
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
        # with open(join(sys.path[0], tracker.path_to_log), 'r') as log:
        with open(tracker.path_to_log, 'r') as log:
            lines = log.read()

        self.assertTrue('Test message' in lines)

    def test_update_json(self):
        s = "placeholder"

    def test_update_happend(self):
        s = "placeholder"

    def test_shut_down(self):
        s = "placeholder"

    def test_write_to_storage(self):
        s = "placeholder"

    def test_update_current_state(self):
        s = "placeholder"

    def test_update_tracked_files_list(self):
        s = "placeholder"

    def test_run_shell_command(self):
        s = "placeholder"

    def test_run_tracker(self):
        s = "placeholder"

if __name__ == '__main__':
    unittest.main()
