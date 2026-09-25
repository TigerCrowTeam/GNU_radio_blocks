import numpy as np
from gnuradio import gr
import pmt

class SyncInserter(gr.basic_block):
    """
    SiK Sync Inserter.
    Prepends a Preamble and Sync Word to every PDU.
    Typically used after whitening, as the preamble and sync word are
    sent as clear bits for the receiver's hardware correlator.
    """
    def __init__(self, preamble_len=16, sync_word=[0x2D, 0xD4]):
        gr.basic_block.__init__(
            self,
            name="SiK Sync Inserter",
            in_sig=None,
            out_sig=None
        )
        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handle_msg)

        # Preamble: repeating 0xAA (10101010) training sequence
        p_bytes = [int(0xAA)] * int(preamble_len)
        s_bytes = [int(b) for b in sync_word]
        self.header = bytes(p_bytes + s_bytes)

    def handle_msg(self, msg):
        if not pmt.is_pair(msg): return

        meta = pmt.car(msg)
        data_pmt = pmt.cdr(msg)

        if not pmt.is_u8vector(data_pmt): return

        whitened_packet = bytes(pmt.u8vector_elements(data_pmt))

        # [Preamble] [Sync Word] [WHITENED_DATA...]
        final_packet = self.header + whitened_packet

        out_pdu = pmt.cons(meta, pmt.init_u8vector(len(final_packet), list(final_packet)))
        self.message_port_pub(pmt.intern("pdus"), out_pdu)
