#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

filename = sys.argv[1]
#mem = cpu.load_memory(filename)
#cpu.run(mem)

cpu.load_memory(filename)
cpu.run()