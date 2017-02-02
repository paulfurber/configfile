
## ConfigFile

  This is ConfigFile, a simple alternative to Python 2.7.x's
  ConfigFileParser.


## Rationale

  I configure my customers' boxes using a couple of standard config
  files. Python's ConfigFileParser has been fine but does have some
  limitations: it doesn't preserve comments or blank lines, it forces
  every option to have an associated section and is somewhat
  over-engineered for what I need. So here for your pleasure is
  ConfigFile.


## Features

  - Read and write configuration files
  - Comments, option=value, single_options, [Section Headers], and blank
    lines recognised
  - Comments and blank lines are detected and preserved when writing
    back to disk
  - The top section of the file does not need a section header
  - Blank config files may be created in memory and written to disk if
    required
  - Sections and options may be freely added, removed or changed
  - Uses the same regexes as ConfigFileParser


## Example

```python

    from ConfigFile import ConfigFile
    c = ConfigFile()
    c.read('config.txt')
    c.get_opt('Main', 'arm_freq')
    
    
## Tests

  In the test/ directory.
  
  
## TODO

ConfigFile should work on Windows with ini files but I haven't tested
it yet. 

Some things like file reading and writing needs to be made more
Pythonic. 

Contributions welcome!

