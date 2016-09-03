

import re


# types of config line
COMMENT = 0   # this is a comment
OPTVAL = 1    # option=value
OPTNV = 2     # option
BLANK = 3     #
SECTION = 4   # [Main]


#
# Regular expressions for parsing section headers and options.
# Shamelessly stolen from Python 2.7 ConfigParser.py
#

SECTCRE = re.compile(
    r'\['                                 # [
    r'(?P<header>[^]]+)'                  # very permissive!
    r'\]'                                 # ]
)
OPTVALRE = re.compile(
    r'(?P<option>[^:=\s][^:=]*)'          # very permissive!
    r'\s*(?P<separator>[:=])\s*'          # any number of space/tab,
                                          # followed by separator
                                          # (either : or =), followed
                                          # by any # space/tab
    r'(?P<value>.*)$'                     # everything up to eol
)
OPTNVRE = re.compile(
    r'(?P<option>[^:=\s][^:=]*)'          # very permissive!
    r'\s*(?:'                             # any number of space/tab,
    r'(?P<separator>[:=])\s*'             # optionally followed by
                                          # separator (either : or
                                          # =), followed by any #
                                          # space/tab
    r'(?P<value>.*))?$'                   # everything up to eol
)

# Error reporting

class FileReadError(Exception):

    def __init__(self, filename):

        Exception.__init__(self, "Problem reading file: %s" % filename)

class FileWriteError(Exception):

    def __init__(self, filename):

        Exception.__init__(self, "Problem writing file: %s" % filename)

        
class ParseError(Exception):

    def __init__(self, line):

        Exception.__init__(self, "Could not parse line: %s" % line)

class UnknownSectionError(Exception):

    def __init__(self, section):

        Exception.__init__(self, "No section with name %s" % section)

class SectionExistsError(Exception):

    def __init__(self, section):

        Exception.__init__(self, "Section exists with name %s" % section)

        
class UnknownOptionError(Exception):

    def __init__(self, option):

        Exception.__init__(self, "No option with name %s" % option)

class DuplicateOptionError(Exception):

    def __init__(self, section, opt):

        Exception.__init__(self, "Option %s in section %s already" % (opt, section))

        
class ConfigLine:


    def __init__(self, line, COMMENTCHAR='#'):

        """Holds a single line of a config file"""

        self.COMMENTCHAR = COMMENTCHAR
        self.section_name = None
        self.option = None
        self.value = None
        self.rawline = line.strip()
        self.linetype = self._gettype()


    def _gettype(self):

        """Parse line and detect its type"""
        
        if self.rawline.startswith(self.COMMENTCHAR):
            return COMMENT

        if self.rawline.isspace() or self.rawline == '':
            return BLANK

        section_match = SECTCRE.match(self.rawline)
        if section_match:
            self.section_name = section_match.group('header')
            return SECTION

        optval_match = OPTVALRE.match(self.rawline)
        if optval_match:
            option, separator, value = optval_match.group('option', 'separator', 'value')
            self.option = option.strip()
            self.value = value.strip()
            return OPTVAL

        optvalnv_match = OPTNVRE.match(self.rawline)
        if optvalnv_match:
            option, separator, value = optvalnv_match.group('option', 'separator', 'value')
            self.option = option.strip()
            return OPTNV

        raise ParseError(self.rawline)

    def set_section(self, section):

        self.section_name = section

    def write(self, f):

        """Write line to a file pointer"""
        
        if self.linetype == SECTION:
            f.write('[%s]\n' % self.section_name)
            return

        if self.linetype == BLANK:
            f.write('\n')
            return

        if self.linetype == COMMENT:
            f.write(self.rawline + '\n')
            return

        if self.linetype == OPTVAL:
            f.write("%s = %s\n" % (self.option, self.value))
            return
        
        if self.linetype == OPTNV:
            f.write("%s" % self.option)
            return

            
    def __str__(self):

        """Sensible string representation"""

        if self.linetype == SECTION:
            return ("Section header: %s" % self.section_name)

        if self.linetype == BLANK:
            return ("Blank line")
        
        if self.linetype == COMMENT:
            return ("Comment: %s" % self.rawline)
        
        if self.linetype == OPTVAL:
            return ("Optval: %s %s" % (self.option, self.value))

        if self.linetype == OPTVALNV:
            return ("Opt: %s " % self.option)

        return "Unknown line type"
    


class ConfigFile:

    
    def __init__(self, COMMENTCHAR='#', nosection_name = 'nosection'):

        """
        A configuration file class. 
        """
        
        self.configlines = []
        self.infile = None
        self.COMMENTCHAR = COMMENTCHAR
        self.nosection_name = nosection_name
        self.sections = []


    def read(self, infile=None):

        
        # if no infile then we just start with a blank ConfigFile
        if infile is None:
            return

        
        self.filename = infile
        try:
            f = open(infile, "rb")
            self.rawlines = f.readlines()
            f.close()
        except:
            raise FileReadError(infile)

        section_name = self.nosection_name
        self.sections = [section_name]
        for line in self.rawlines:
            cl = ConfigLine(line, self.COMMENTCHAR)
            if cl.section_name is None:
                cl.section_name = section_name
            else:
                section_name = cl.section_name
                self.sections.append(section_name)
            
            self.configlines.append(cl)

    def opt_exists(self, section, opt):

        if section not in self.sections:
            return False

        for l in self.configlines:
            if l.section_name == section and l.linetype == OPTVAL:
                if opt == l.option:
                    return True

        return False
            
    def set_opt(self, section, opt, val):

        if section not in self.sections:
            raise UnknownSectionError(section)

        for l in self.configlines:
            if l.section_name == section and l.linetype == OPTVAL:
                if opt == l.option:
                    l.value = val
                    return

        raise UnknownOptionError(opt)

    def get_opt(self, section, opt):

        if section not in self.sections:
            raise UnknownSectionError(section)

        for l in self.configlines:
            if l.section_name == section and l.linetype == OPTVAL:
                if opt == l.option:
                    return l.value

        raise UnknownOptionError(opt)

    
    def add_opt(self, section, opt, val):

        if section not in self.sections:
            raise UnknownSectionError(section)

        if self.opt_exists(section, opt):
            raise DuplicateOptionError(section, opt)
            
        line = '%s = %s' % (opt, val)
            
        for l in self.configlines:
            if l.section_name == section:
                cl = ConfigLine(line)
                cl.section_name = section
                self.configlines.append(cl)
                return

    def add_optnv(self, section, opt):

        if section not in self.sections:
            raise UnknownSectionError(section)

        if self.opt_exists(section, opt):
            raise DuplicateOptionError(section, opt)
            
        line = '%s' % opt
            
        for l in self.configlines:
            if l.section_name == section:
                cl = ConfigLine(line)
                cl.section_name = section
                self.configlines.append(cl)
                return

            
    def add_section(self, section):

        if section in self.sections:
            raise SectionExistsError(section)

        self.sections.append(section)

        # add a leading blank line
        blank = ConfigLine('\n')
        blank.set_section(section)
        self.configlines.append(blank)
        # now add the new section
        self.configlines.append(ConfigLine('[%s]' % section))
        

    def save(self, filename=''):

        if filename is not '':
            self.filename = filename

        try:
            f = open(self.filename, "wb")
            for section in self.sections:
                for line in self.configlines:
                    if line.section_name == section:
                        line.write(f)
            f.close()
        except:
            raise FileWriteError(self.filename)
        




if __name__ == '__main__':

        c = ConfigFile()
        c.read('config.txt')

        print c.sections
        

        c.set_opt('Main', 'arm_freq', '1000')
        c.add_section('PI')
        c.add_opt('PI', 'boot', 'fast')
                

        c.save('config.out')

        for l in c.configlines:
            print "Section: %s %s" % (l.section_name, str(l))

        print c.get_opt('Main', 'arm_freq')
        print c.get_opt('Main', 'network_init_order').split(',')

        c2 = ConfigFile()
        c2.add_section('Main')
        c2.add_opt('Main', 'a_parm', 'a_value')

        c2.add_section('Another Section')
        c2.add_optnv('Another Section', 'anotherparm')

        c2.save('new_config.txt')
