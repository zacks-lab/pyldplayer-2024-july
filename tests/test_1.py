from time import sleep
import unittest
from pyldplayer import LDPlayer, LDInstance

client : LDPlayer

class t_ldplayer(unittest.TestCase):
    def setUp(self):
        global client
        client = LDPlayer()

    def test_list(self):
        print(client.list())
        self.assertTrue(len(client.list()) > 0)

    def test_list2(self):
        res = client.list2()
        self.assertTrue(len(res) > 0)
        self.assertIsInstance(res[0], LDInstance)

    @unittest.skip("skip")
    def test_quit(self):
        res = client.list2()
        try:
            res[0].quit()
        except: # noqa
            pass
        
        self.assertFalse(res[0].android_started)
        res[0].launch()
        #sleep(15)
        #elf.assertTrue(res[0].android_started)
        sleep(10)
        res[0].quit()   
        #self.assertFalse(res[0].android_started)
        
    @unittest.skip("skip")
    def test_copy(self):
        res = client.listInstances()
        client.copy("test", res[3])

    @unittest.skip("skip, too costly")
    def test_copy_and_delete(self):
        ores = client.listInstances()
        client.copy("test_xxx", ores[-1])
        res = client.listInstances()

        self.assertTrue(len(res) > len(ores))

        # delete all test sss
        for i in res:
            if i.name == "test_xxx":
                i.delete()
        
        sleep(5)

        newres = client.listInstances()
        self.assertTrue(len(newres) == len(ores))

