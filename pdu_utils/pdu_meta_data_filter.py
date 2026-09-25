"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

"""
Takes an incoming PDU and checks its metadata for a user-defined key/value pair. 
The complete PDU is forwarded only when the metadata matches; otherwise, it is discarded.
"""

import numpy as np
from gnuradio import gr
import pmt
import sys

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, key = 'PDU', value = 1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='PDU Metadata Filter',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.key = key
        self.value = value

        self.message_port_register_in(pmt.intern("Input"))
        self.set_msg_handler(pmt.intern("Input"),self.filter_pdu)

        self.message_port_register_out(pmt.intern("Output"))

    def filter_pdu(self,pdu):
        try:
            meta = pmt.car(pdu)
            data = pmt.cdr(pdu)
            ref = pmt.dict_ref(meta, pmt.intern(self.key), pmt.PMT_NIL)
            if pmt.to_python(ref) == self.value:
                self.message_port_pub(pmt.intern("Output"), pmt.cons(meta, data))
        except Exception as e:
            _, _, exc_tb = sys.exc_info()
            line_number = exc_tb.tb_lineno
            print(f"Error validating PDU: Line {line_number} : {e}")
