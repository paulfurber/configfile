from distutils.core import setup

setup(name = "ConfigFile",
    version = "0.1",
    description = "Python module to read text configuration files",
    author = "Paul Furber",
    author_email = "paul.furber@gmail.com",
    url = "http://github.com/paulfurber/configfile",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages = ['ConfigFile'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.

) 
