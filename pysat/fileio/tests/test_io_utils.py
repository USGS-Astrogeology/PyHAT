import os
import unittest

from .. import io_utils


class TestIoUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_and_destroy_directory(self):
        path = io_utils.create_dir()
        self.assertTrue(os.path.exists(path))
        io_utils.delete_dir(path)
        self.assertFalse(os.path.exists(path))
