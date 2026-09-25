"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

"""Decimates an incoming stream by a user-defined integer factor `N`, keeping every Nth sample. 
Sample type is user-selectable (`float` or `complex`) so the same block can be used on real or complex signals."""

import numpy as np
from gnuradio import gr
import sys

class blk(gr.decim_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple decimator"""

    def __init__(self, type = "float", N = 1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        self.type_map = {
            "float": np.float32,
            "complex": np.complex64,
        }
        selected_type = self.type_map.get(type, np.float32)
        self.N = N

        gr.decim_block.__init__(
            self,
            name='Decimator',
            in_sig=[selected_type], 
            out_sig=[selected_type],
            decim=self.N
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

    def work(self, input_items, output_items):
        try:
            """decimates a signal by a user-defined integer amount"""
            output_items[0][:] = input_items[0][::self.N]
            return len(output_items[0])
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            print(f"Error Decimating Signal at: {line_number} : {e}")
            return 0
