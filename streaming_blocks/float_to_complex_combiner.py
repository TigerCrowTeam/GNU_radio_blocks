"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

"""Combines two `float32` streams into a single `complex64` stream. 
Input port 0 becomes the real (I) component and port 1 becomes the imaginary (Q) component of each output sample."""

import numpy as np
from gnuradio import gr
import sys

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Float To Complex',   # will show up in GRC
            in_sig=[np.float32, np.float32], # [0]=real (I), [1]=imag (Q)
            out_sig=[np.complex64]
        )

    def work(self, input_items, output_items):
        try:
            """combine two float32 streams into a complex64 stream"""
            output_items[0][:] = input_items[0] + 1j * input_items[1]
            return len(output_items[0])
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            print(f"Error Combining Float to Complex Signal at: {line_number} : {e}")
            return 0
