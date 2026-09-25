"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
"""Visit for documentation on stream tags: https://wiki.gnuradio.org/index.php/Stream_Tags"""

import numpy as np
from gnuradio import gr
import sys
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple power tagger"""

    def __init__(self, threshold=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Power Tagger',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.complex64]
        )
        self.threshold = threshold

    def work(self, input_items, output_items):
        try:
            """Output the power of the IQ stream"""
            for indx, sample in enumerate(input_items[0]):
                output_items[0][indx] = np.abs(sample) ** 2 # reversing the quadrature equation back to I^2 + Q^2.
                if output_items[0][indx] > self.threshold: # example condition, tag if power exceeds threshold
                    self.add_item_tag(0,
                        self.nitems_written(0) + indx,
                        pmt.intern("high_power"),
                        pmt.intern(float(output_items[0][indx]))
                    )
            return len(output_items[0])
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            print(f"Error tagging power at: {line_number} : {e}")
            return 0