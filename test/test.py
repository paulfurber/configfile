


import unittest
from ConfigFile import ConfigFile

class TestConfigFileRead(unittest.TestCase):

        def test_read_sections(self):

             c = ConfigFile()
             c.read('config.txt')
             assert(c.sections == ['topsection', 'Main'])

        def test_read_values(self):
                
             c = ConfigFile()
             c.read('config.txt')
             assert(c.get_opt('Main', 'arm_freq') == '900')
             assert(c.get_opt('Main', 'network_init_order').split(',') == ['eth0', 'wlan0', 'usb0'])

class TestConfigFileWrite(unittest.TestCase):

        pass


        

                         

if __name__ == '__main__':

        unittest.main()
        
        # c.set_opt('Main', 'arm_freq', '1000')
        # c.add_section('PI')
        # c.add_opt('PI', 'boot', 'fast')
        # c.save('config.out')

        # for l in c.configlines:
        #         print "Section: %s %s" % (l.section_name, str(l))

        # print c.get_opt('Main', 'arm_freq')
        # print c.get_opt('Main', 'network_init_order').split(',')

        # c2 = ConfigFile()
        # c2.add_section('Main')
        # c2.add_opt('Main', 'a_parm', 'a_value')

        # c2.add_section('Another Section')
        # c2.add_optnv('Another Section', 'anotherparm')

        # c2.save('new_config.txt')
