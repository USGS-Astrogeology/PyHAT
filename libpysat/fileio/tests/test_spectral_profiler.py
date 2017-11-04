import unittest

from libpysat.examples import get_path

from .. import io_spectral_profiler as sp


class Test_Spectral_Profiler_IO(unittest.TestCase):
    def setUp(self):
        self.examplefile = get_path('SP_2C_02_02358_S138_E3586.spc')

    def test_openspc(self):
        dataset = sp.Spectral_Profiler(self.examplefile)
        # self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
