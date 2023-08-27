import unittest

from pyldplayer import LDPlayer
from pyldplayer.mapping import SMP, LDKeyboardMapping, Record
class T_mappings(unittest.TestCase):
    def test_smp(self):
        player = LDPlayer()
        smps = player.getSMPS()
        self.assertTrue(all(isinstance(i, SMP) for i in smps.values()))

    def test_kmp(self):
        player = LDPlayer()
        kmps = player.getKMPS()
        self.assertTrue(all(isinstance(i, LDKeyboardMapping) for i in kmps.values()))

    def test_record(self):
        player = LDPlayer()
        records = player.getRecords()
        self.assertTrue(all(isinstance(i, Record) for i in records.values()))
