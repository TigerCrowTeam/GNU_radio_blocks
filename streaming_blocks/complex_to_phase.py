"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

"""Converts a complex IQ stream to its phase representation. 
If you want to display the magnitude as well, you can modify the 
block to output both phase and magnitude.""" 

import numpy as np
from gnuradio import gr
import math as math
import sys

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Complex to Phase',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.float32] # if you want to also output the quadrature, add: ", float32"
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def work(self, input_items, output_items):
        try:
            """Output the phase of the IQ stream"""
            output_items[0][:] = np.angle(input_items[0])
            #output_items[1][:] = np.abs(input_items[0]) #output for the quadrature, np.abs gives the magnitude: sqrt(3^2 + 4^2) = sqrt(25)
            return len(output_items[0])
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            print(f"Error Decimating Signal at: {line_number} : {e}")
            return 0
