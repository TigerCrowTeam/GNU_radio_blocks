import numpy as np
from gnuradio import gr
import pmt
import struct

class Framer(gr.basic_block):
    """
    SiK Radio PDU Framer (Sandia v3.x Specifications).
    Constructs: [NET_ID(2 BE)] [LEN(2 LE)] [PAYLOAD] [TRAILER(3)] [CRC(2 LE)]
    
    Verified behavior for Sandia extraction:
    - NetID: 19 (0x0013)
    - LEN: Payload Length + 3 (Trailer)
    - Trailer: Configurable (often 00 00 00 or specific hardware tags)
    - CRC: CRC16-CCITT (Poly 0x8005, Init 0x0000, non-reflected)
    """
    def __init__(self, net_id=19, trailer=[0x8e, 0x1c, 0x49]):
        gr.basic_block.__init__(self, name="SiK PDU Framer v2", in_sig=None, out_sig=None)
        
        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self.handle_msg)

        self.net_id = int(net_id)
        self.trailer = bytes(trailer)

    def calculate_crc16(self, data):
        """
        CRC16 calculator: Standard 0x8005 (non-reflected, initial 0x0000).
        """
        poly = 0x8005
        crc = 0x0000
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
        return crc & 0xFFFF

    def handle_msg(self, msg):
        if not pmt.is_pair(msg): return
        meta, payload_pmt = pmt.car(msg), pmt.cdr(msg)
        if not pmt.is_u8vector(payload_pmt): return

        payload = bytes(pmt.u8vector_elements(payload_pmt))
        
        # LEN field in SiK includes the payload length + the 3-byte trailer
        total_len_field = len(payload) + len(self.trailer)
        
        # Construct Header: NetID (Big-Endian), Len (Little-Endian)
        header = struct.pack('>H', self.net_id) + struct.pack('<H', total_len_field)
        
        # Assemble packet body
        packet_body = header + payload + self.trailer
        
        # Calculate CRC over the body
        crc = self.calculate_crc16(packet_body)
        
        # Final Packet: Body + CRC (Little-Endian)
        final_packet = packet_body + struct.pack('<H', crc)
        
        out_pdu = pmt.cons(meta, pmt.init_u8vector(len(final_packet), list(final_packet)))
        self.message_port_pub(pmt.intern("pdus"), out_pdu)