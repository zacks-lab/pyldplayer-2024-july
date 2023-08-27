
import unittest
from pyldplayer import LDPlayerConfig

class t_config(unittest.TestCase):
    def test_config_1(self):
        config = LDPlayerConfig(
            resolution=(1280, 720, 240),
        )

        cmd = config.toCommand()
        self.assertEqual(cmd, ["--resolution", "1280,720,240"])

    def test_config_2(self):
        config = LDPlayerConfig(
            imei=LDPlayerConfig.AUTO,
        )

        cmd = config.toCommand()
        self.assertEqual(cmd, ["--imei", "auto"])