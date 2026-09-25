import numpy as np
from gnuradio import gr
import pmt

class universal_whitener(gr.basic_block):
    """
    A Universal PDU Whitener matching the 'perfect' Dewhitener.
    
    This block is the inverse of block_1's (unpack_big -> XOR -> pack_little).
    To be the true inverse, this block must do: (unpack_little -> XOR -> pack_big).
    """
    def __init__(self, order=9, taps=[9, 4, 0], seed_str="111111111", bit_order='msb'):
        gr.basic_block.__init__(
            self,
            name="Universal Whitener v2",
            in_sig=None,
            out_sig=None
        )
        
        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handle_msg)

        self.order = order
        self.taps = taps
        self.seed_str = seed_str
        self.bit_order = bit_order.lower()

    def generate_lfsr_mask(self, num_bits):
        state = [int(b) for b in self.seed_str]
        mask = np.zeros(num_bits, dtype=np.uint8)
        for i in range(num_bits):
            out_bit = state[-1]
            mask[i] = out_bit
            fb = 0
            for t in self.taps:
                if t == 0: continue
                fb ^= state[t-1]
            state = [fb] + state[:-1]
        return mask

    def handle_msg(self, msg):
        if not pmt.is_pair(msg): return
        meta, data_pmt = pmt.car(msg), pmt.cdr(msg)
        if not pmt.is_u8vector(data_pmt): return

        in_data = np.array(pmt.u8vector_elements(data_pmt), dtype=np.uint8)
        
        # To inverse (unpack_big -> XOR -> pack_little), we do:
        # (unpack_little -> XOR -> pack_big)
        
        # 1. Unpack bits (ALWAYS little for the inverse of block_1's pack_little)
        bits = np.unpackbits(in_data, bitorder='little')
            
        # 2. XOR
        mask = self.generate_lfsr_mask(len(bits))
        processed_bits = bits ^ mask
        
        # 3. Repack bits (ALWAYS big for the inverse of block_1's unpack_big)
        processed_bytes = np.packbits(processed_bits, bitorder='little')
            
        out_pdu = pmt.cons(meta, pmt.init_u8vector(len(processed_bytes), processed_bytes))
        self.message_port_pub(pmt.intern("pdus"), out_pdu)