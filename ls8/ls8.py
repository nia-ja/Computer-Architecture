#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# cpu = CPU()

# cpu.load()
# cpu.run()
with open('./examples/mult.ls8') as program:
    cpu = CPU()
    cpu.load(program)
    cpu.run()