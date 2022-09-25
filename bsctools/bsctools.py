'''
bsctools - a single cell bacteria transcripton analysis pipeline
====================================================================

:Author:  
:Release: bioinplant
:Date:    2022.09.15
:Tags:    Bacteria SCRNA-seq analysis pipeline

There are 3 tools:

  - inanno       This tools based on kraken2 to do species identification
  - pandb        Dataset of bacteria pangenome in genus level
  - pang         Pan-genome test

To get help on a specific tool, type:

	bsctools <tools> --help

To use a specific tools, type:

	bsctools <tool> [tools options] [tool argument]
'''

from __future__ import absolute_import
import os
import sys
import importlib
from bsctools import __version__

def main(argv = None):

  argv = sys.argv

  path = os.path.abspath(os.path.dirname(__file__))

  if len(argv) == 1 or argv[1] == "--help" or argv[1] == "-h":
    print(globals()["__doc__"])

    return

  elif len(argv) ==1 or argv[1] == "--version" or argv[1] == "-v":
    print("bsctools version: %s" % __version__)

    return

  elif argv[2] in ["--help", "-h", "--help-extended"]:
    print("bsctools: Version %s" % __version__)

  command = argv[1]

  module = importlib.import_module("bsctools." + command, "bsctools")
  ##remove 'bsctools' from sys.argv
  del sys.argv[0]
  module.main(sys.argv)

if __name__ == '__main__':
  sys.exit(main())
